import uuid

import pytest

from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.listing.presentation.dto import ChangeListingAttributeRequest


class TestChangeListingPriceUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_listing_price_success(
        self,
        create_listing_usecase,
        change_listing_attribute_usecase,
        create_organization,
        listing_repository,
        create_listing_request,
    ):
        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_organization.owner_id, dto)

        change_attribute_dto = ChangeListingAttributeRequest(
            subcategory_id=create_listing_request.subcategory_id,
            attributes={
                "engine_power": 123,
                "brand": "John Deere",
                "year_of_issue": 2024,
                "condition": "used",
            },
        )
        await change_listing_attribute_usecase.execute(create_organization.owner_id, listing_id, change_attribute_dto)

        listing_after = await listing_repository.get_by_id(listing_id)
        assert listing_after.attributes["engine_power"] == 123

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_attributes_rejects_foreign_subcategory(
        self,
        create_listing_usecase,
        change_listing_attribute_usecase,
        create_organization,
        listing_repository,
        create_listing_request,
    ):
        listing_id = await create_listing_usecase.execute(create_organization.owner_id, create_listing_request)

        dto = ChangeListingAttributeRequest(subcategory_id=uuid.uuid4(), attributes={"engine_power": 123})
        with pytest.raises(CatalogNotFoundError):
            await change_listing_attribute_usecase.execute(create_organization.owner_id, listing_id, dto)

        listing_after = await listing_repository.get_by_id(listing_id)
        assert listing_after.attributes["engine_power"] == create_listing_request.attributes["engine_power"]
