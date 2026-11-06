import re
from uuid import UUID

from src.core.listing.domain.entities import Listing
from src.core.listing.domain.exceptions import ListingInvalidFilterKeyError
from src.core.listing.presentation.dto import ListingSearchDocument, ListingSearchQuery
from src.core.shared.infrastructure.services.meilisearch_service import (
    MeilisearchService,
)
from src.core.shared.presentation.dto import SearchIndexConfig, SearchResult


class ListingSearchService:
    INDEX_NAME = "listing"
    FILTERABLE: list[str] = [
        "is_active",
        "subcategory_id",
        "city_id",
        "price",
        "currency",
    ]
    SORTABLE: list[str] = ["price", "created_at"]
    SEARCHABLE: list[str] = ["title", "description"]
    # Ключ атрибута попадает в выражение фильтра без кавычек, поэтому допускаем только идентификатор.
    FILTER_KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

    def __init__(self, search_service: MeilisearchService):
        self.search_service = search_service

    async def index_listing(self, listing: Listing, attributes: dict) -> None:
        document = ListingSearchDocument.from_listing(listing, attributes)
        await self.search_service.index_documents(index_name=self.INDEX_NAME, documents=[document.model_dump()])

    async def remove_listing(self, listing_id: UUID) -> None:
        await self.search_service.delete_documents(
            index_name=self.INDEX_NAME,
            document_ids=[str(listing_id)],
        )

    async def search_listings(self, query: ListingSearchQuery) -> SearchResult:
        return await self.search_service.search(
            index_name=self.INDEX_NAME,
            query=query.text,
            filter_expression=self.build_filter(query),
            page=query.page,
            limit=query.limit,
        )

    async def sync_schema(self, dynamic_filters: list[str]) -> None:
        config = SearchIndexConfig(
            filterable=self.FILTERABLE + dynamic_filters,
            sortable=self.SORTABLE,
            searchable=self.SEARCHABLE,
        )

        return await self.search_service.configure_index(
            index_name=self.INDEX_NAME,
            index_config=config,
        )

    def build_filter(self, query: ListingSearchQuery) -> list[str]:
        filters = ["is_active = true"]

        if query.subcategory_id:
            filters.append(f"subcategory_id = {self._format_value(str(query.subcategory_id))}")
        if query.city_id:
            filters.append(f"city_id = {self._format_value(str(query.city_id))}")
        if query.price_min is not None:
            filters.append(f"price >= {query.price_min}")
        if query.price_max is not None:
            filters.append(f"price <= {query.price_max}")
        for key, value in query.attributes.items():
            if not self.FILTER_KEY_PATTERN.fullmatch(key):
                raise ListingInvalidFilterKeyError(key)
            filters.append(f"{key} = {self._format_value(value)}")

        return filters

    @staticmethod
    def _format_value(value: str | int | float | bool) -> str:
        """Значение для выражения фильтра Meilisearch: строки в кавычках с экранированием."""
        # bool проверяем раньше int: в Python bool это подкласс int.
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        # Обратный слэш экранируем первым, иначе он «съест» закрывающую кавычку.
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
