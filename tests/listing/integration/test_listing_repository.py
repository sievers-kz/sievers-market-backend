import uuid

import pytest

from src.core.listing.domain.entities import Listing
from src.core.listing.domain.enums import ListingStatus


class TestListingRepository:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_and_get_by_id(self, listing_repository, create_listing):
        listing = create_listing
        result = await listing_repository.get_by_id(listing.id)

        assert result is not None
        assert result.id == listing.id
        assert isinstance(result, Listing)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_id_returns_none_for_unknown(self, listing_repository):
        result = await listing_repository.get_by_id(uuid.uuid4())
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_updates_existing_listing(
        self, listing_repository, create_listing
    ):
        listing = create_listing
        listing.change_price(9000000, listing.currency)
        await listing_repository.save(listing)

        updated = await listing_repository.get_by_id(listing.id)
        assert updated.price == 9000000

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_updates_status(self, listing_repository, create_listing):
        listing = create_listing
        listing.deactivate()
        await listing_repository.save(listing)

        updated = await listing_repository.get_by_id(listing.id)
        assert updated.status == ListingStatus.INACTIVE
