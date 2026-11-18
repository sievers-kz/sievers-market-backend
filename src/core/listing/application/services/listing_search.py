import re
from uuid import UUID

from src.core.catalog.infrastructure.catalog_service import CatalogService
from src.core.catalog.infrastructure.enums import AttributeType
from src.core.listing.domain.entities import Listing
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import (
    ListingAttributeFilterWithoutSubcategoryError,
    ListingInvalidFilterKeyError,
    ListingInvalidRangeFilterError,
)
from src.core.listing.presentation.dto import (
    ListingSearchDocument,
    ListingSearchQuery,
    ListingSearchSort,
)
from src.core.shared.domain.enums import PriceCurrency
from src.core.shared.infrastructure.services.meilisearch_service import (
    MeilisearchService,
)
from src.core.shared.presentation.dto import SearchIndexConfig, SearchResult


class ListingSearchService:
    INDEX_NAME = "listing"
    FILTERABLE: list[str] = [
        "is_active",
        "category_id",
        "subcategory_id",
        "city_id",
        "price",
        "currency",
    ]
    SORTABLE: list[str] = ["price", "created_at"]
    SEARCHABLE: list[str] = ["title", "description"]
    # Ключ атрибута попадает в выражение фильтра без кавычек, поэтому допускаем только идентификатор.
    FILTER_KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
    NUMERIC_TYPES = frozenset({AttributeType.INTEGER, AttributeType.FLOAT})
    PRICE_SORTS = frozenset({ListingSearchSort.PRICE_ASC, ListingSearchSort.PRICE_DESC})
    SORT_RULES: dict[ListingSearchSort, list[str]] = {
        ListingSearchSort.NEWEST: ["created_at:desc"],
        ListingSearchSort.PRICE_ASC: ["price:asc"],
        ListingSearchSort.PRICE_DESC: ["price:desc"],
    }

    def __init__(self, search_service: MeilisearchService, catalog_service: CatalogService):
        self.search_service = search_service
        self.catalog_service = catalog_service

    async def sync_listing(self, listing: Listing) -> None:
        """Приводит индекс в соответствие с объявлением после любого изменения.

        Активное объявление индексируется только с фильтруемыми атрибутами подкатегории;
        неактивное, архивное или удалённое убирается из индекса, чтобы не попадать в поиск.
        """
        if listing.status != ListingStatus.ACTIVE:
            await self.remove_listing(listing.id)
            return

        filterable_keys = await self.catalog_service.get_filterable_keys(listing.subcategory_id)
        document = self.build_document(listing, filterable_keys)
        await self.search_service.index_documents(index_name=self.INDEX_NAME, documents=[document.model_dump()])

    async def index_listings(self, listings: list[Listing]) -> int:
        """Пачкой индексирует активные объявления (для переиндексации). Возвращает число документов.

        Фильтруемые ключи запрашиваются один раз на подкатегорию, а не на каждое объявление.
        """
        keys_by_subcategory: dict[UUID, set[str]] = {}
        documents = []
        for listing in listings:
            if listing.status != ListingStatus.ACTIVE:
                continue
            if listing.subcategory_id not in keys_by_subcategory:
                keys_by_subcategory[listing.subcategory_id] = await self.catalog_service.get_filterable_keys(
                    listing.subcategory_id
                )
            document = self.build_document(listing, keys_by_subcategory[listing.subcategory_id])
            documents.append(document.model_dump())

        if documents:
            await self.search_service.index_documents(index_name=self.INDEX_NAME, documents=documents)
        return len(documents)

    async def clear_index(self) -> None:
        await self.search_service.delete_all_documents(index_name=self.INDEX_NAME)

    @staticmethod
    def build_document(listing: Listing, filterable_keys: set[str]) -> ListingSearchDocument:
        attributes = {key: value for key, value in listing.attributes.items() if key in filterable_keys}
        return ListingSearchDocument.from_listing(listing, attributes)

    async def remove_listing(self, listing_id: UUID) -> None:
        await self.search_service.delete_documents(
            index_name=self.INDEX_NAME,
            document_ids=[str(listing_id)],
        )

    async def search_listings(self, query: ListingSearchQuery) -> SearchResult:
        """Подходящие объявления в нужном порядке. В `hits` только `id`: карточки собираются из Postgres."""
        await self.validate_attribute_keys(query)

        return await self.search_service.search(
            index_name=self.INDEX_NAME,
            query=query.text,
            filter_expression=self.build_filter(query),
            page=query.page,
            limit=query.limit,
            sort=self.build_sort(query),
            attributes_to_retrieve=["id"],
        )

    async def validate_attribute_keys(self, query: ListingSearchQuery) -> None:
        """Фильтр по атрибуту допустим, только если атрибут фильтруемый в выбранной подкатегории.

        Иначе Meilisearch ответит ошибкой «атрибут не фильтруемый», и клиент получит 500 вместо понятной 422.
        """
        if not query.attributes and not query.attribute_ranges:
            return
        if query.subcategory_id is None:
            raise ListingAttributeFilterWithoutSubcategoryError()

        filterable_types = await self.catalog_service.get_filterable_types(query.subcategory_id)
        for key in [*query.attributes, *query.attribute_ranges]:
            if key not in filterable_types:
                raise ListingInvalidFilterKeyError(key)
        for key in query.attribute_ranges:
            # Диапазон по строке или списку Meilisearch сравнил бы лексикографически, это бессмыслица.
            if filterable_types[key] not in self.NUMERIC_TYPES:
                raise ListingInvalidRangeFilterError(key)

    def build_sort(self, query: ListingSearchQuery) -> list[str] | None:
        if query.sort is not None:
            return self.SORT_RULES[query.sort]
        # С текстом оставляем порядок по релевантности, без текста показываем новые.
        return None if query.text else self.SORT_RULES[ListingSearchSort.NEWEST]

    async def sync_schema(self) -> None:
        """Настройки индекса: что фильтруется, сортируется и где ищется текст.

        Фильтруемые атрибуты берутся из флагов `filterable` каталога; строковые из них ещё и участвуют
        в текстовом поиске (например, марка, введённая текстом).
        """
        attributes = await self.catalog_service.get_search_attributes()
        config = SearchIndexConfig(
            filterable=self.FILTERABLE + attributes.filterable,
            sortable=self.SORTABLE,
            searchable=self.SEARCHABLE + attributes.text,
        )

        return await self.search_service.configure_index(
            index_name=self.INDEX_NAME,
            index_config=config,
        )

    def build_filter(self, query: ListingSearchQuery) -> list[str]:
        filters = ["is_active = true"]

        if query.category_id:
            filters.append(f"category_id = {self._format_value(str(query.category_id))}")
        if query.subcategory_id:
            filters.append(f"subcategory_id = {self._format_value(str(query.subcategory_id))}")
        if query.city_id:
            filters.append(f"city_id = {self._format_value(str(query.city_id))}")
        if query.price_min is not None:
            filters.append(f"price >= {query.price_min}")
        if query.price_max is not None:
            filters.append(f"price <= {query.price_max}")
        if self._compares_price(query):
            # Временно: `price` хранится в валюте продавца, поэтому сравниваем только тенговые объявления.
            # Когда в документе появится `price_kzt` (курс НБ РК), фильтр и сортировку перевести на него,
            # а это условие убрать: тогда найдутся и объявления в других валютах.
            filters.append(f"currency = {self._format_value(PriceCurrency.KZT.value)}")
        for key, value in query.attributes.items():
            self._check_key(key)
            filters.append(f"{key} = {self._format_value(value)}")
        for key, bounds in query.attribute_ranges.items():
            self._check_key(key)
            if bounds.min is not None:
                filters.append(f"{key} >= {self._format_value(bounds.min)}")
            if bounds.max is not None:
                filters.append(f"{key} <= {self._format_value(bounds.max)}")

        return filters

    def _check_key(self, key: str) -> None:
        # Ключ попадает в выражение без кавычек: второй рубеж после проверки по каталогу.
        if not self.FILTER_KEY_PATTERN.fullmatch(key):
            raise ListingInvalidFilterKeyError(key)

    def _compares_price(self, query: ListingSearchQuery) -> bool:
        return query.price_min is not None or query.price_max is not None or query.sort in self.PRICE_SORTS

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
