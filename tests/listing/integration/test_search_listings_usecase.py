import pytest

from src.core.listing.presentation.dto import ListingSearchQuery
from src.core.shared.presentation.dto import SearchResult


class TestSearchListingsUseCase:
    """Meilisearch подменён моком: проверяем, что карточки собираются из Postgres в порядке поиска."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_cards_in_search_order(
        self,
        container,
        mock_search_service,
        create_listing_usecase,
        create_organization,
        create_listing_request,
    ):
        owner_id = create_organization.owner_id
        first = await create_listing_usecase.execute(owner_id, create_listing_request)
        second = await create_listing_usecase.execute(owner_id, create_listing_request)
        mock_search_service.search.return_value = SearchResult(
            hits=[{"id": str(second)}, {"id": str(first)}],
            total=2,
            page=1,
            pages=1,
        )

        result = await container.listing.search_listings_usecase().execute(ListingSearchQuery())

        assert [card.id for card in result.items] == [second, first]
        assert result.total == 2
        card = result.items[0]
        assert card.title == create_listing_request.title
        assert card.organization_name is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_inactive_listing_skipped(
        self,
        container,
        mock_search_service,
        create_listing_usecase,
        deactivate_listing_usecase,
        create_organization,
        create_listing_request,
    ):
        owner_id = create_organization.owner_id
        active = await create_listing_usecase.execute(owner_id, create_listing_request)
        inactive = await create_listing_usecase.execute(owner_id, create_listing_request)
        await deactivate_listing_usecase.execute(owner_id, inactive)
        mock_search_service.search.return_value = SearchResult(
            hits=[{"id": str(inactive)}, {"id": str(active)}],
            total=2,
            page=1,
            pages=1,
        )

        result = await container.listing.search_listings_usecase().execute(ListingSearchQuery())

        assert [card.id for card in result.items] == [active]
