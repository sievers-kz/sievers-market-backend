import uuid

import pytest
from sqlalchemy import text

from src.core.listing.presentation.dto import ChangeListingLocationRequest


class TestChangeListingPriceUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_listing_price_success(
        self,
        create_listing_usecase,
        change_listing_location_usecase,
        create_vendor,
        listing_repository,
        create_listing_request,
        database_session
    ):
        city_id = (await database_session.execute(text("SELECT id FROM cities LIMIT 1"))).scalar_one()

        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_vendor.id, dto)

        listing = await listing_repository.get_by_id(listing_id)
        change_location_dto = ChangeListingLocationRequest(city_id=city_id)
        await change_listing_location_usecase.execute(create_vendor.id, listing_id, change_location_dto)

        listing_after = await listing_repository.get_by_id(listing_id)
        assert listing_after.city_id == listing.city_id

