import pytest
from sqlalchemy import text

from src.core.listing.presentation.dto import ChangeListingDescriptionRequest, ChangeListingAttributeRequest


class TestChangeListingPriceUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_listing_price_success(
        self,
        create_listing_usecase,
        change_listing_attribute_usecase,
        create_vendor,
        listing_repository,
        create_listing_request,
        database_session,
    ):
        subcategory_id = (await database_session.execute(text("SELECT id FROM subcategories LIMIT 1"))).scalar_one()

        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_vendor.id, dto)

        change_attribute_dto = ChangeListingAttributeRequest(subcategory_id=subcategory_id, attributes={"engine_power": 123})
        await change_listing_attribute_usecase.execute(create_vendor.id, listing_id, change_attribute_dto)

        listing_after = await listing_repository.get_by_id(listing_id)
        assert listing_after.attributes["engine_power"] == 123
