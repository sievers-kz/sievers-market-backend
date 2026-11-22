from uuid import UUID

from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.infrastructure.query import ListingQueryService
from src.core.listing.presentation.dto import ListingCardResponse, ListingSearchQuery
from src.core.shared.presentation.dto import PaginatedResponse


class SearchListingsUseCase:
    """Поиск объявлений: Meilisearch решает, какие подходят и в каком порядке, Postgres собирает карточки.

    Карточки не копируются в индекс, поэтому в ответе всегда свежие данные и тот же формат, что в каталоге.
    """

    def __init__(self, listing_search_service: ListingSearchService, query_service: ListingQueryService):
        self.listing_search_service = listing_search_service
        self.query_service = query_service

    async def execute(self, query: ListingSearchQuery) -> PaginatedResponse[ListingCardResponse]:
        result = await self.listing_search_service.search_listings(query)
        ids = [UUID(hit["id"]) for hit in result.hits]

        cards = await self.query_service.get_listings_by_ids(ids)
        # Postgres возвращает строки в своём порядке; восстанавливаем порядок из Meilisearch.
        cards_by_id = {card.id: card for card in cards}
        items = [cards_by_id[listing_id] for listing_id in ids if listing_id in cards_by_id]

        return PaginatedResponse[ListingCardResponse](
            items=items,
            total=result.total,
            page=result.page,
            pages=result.pages,
        )
