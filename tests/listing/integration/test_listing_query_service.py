import uuid

import pytest

from src.core.listing.domain.exceptions import ListingNotFoundError


@pytest.fixture
def listing_query_service(container):
    return container.listing.query_service()


class TestListingQueryServiceDetails:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_details_of_active_listing(self, listing_query_service, create_listing):
        result = await listing_query_service.get_listing_details(create_listing.id)

        assert result.id == create_listing.id
        assert result.owner_id == create_listing.organization_id
        assert result.title == create_listing.title
        assert result.price == create_listing.price

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_listing_raises_not_found(self, listing_query_service):
        with pytest.raises(ListingNotFoundError):
            await listing_query_service.get_listing_details(uuid.uuid4())
