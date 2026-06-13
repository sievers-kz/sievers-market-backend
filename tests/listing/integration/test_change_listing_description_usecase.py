import pytest

from src.core.listing.presentation.dto import ChangeListingDescriptionRequest


class TestChangeListingPriceUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_listing_price_success(
        self,
        create_listing_usecase,
        change_listing_description_usecase,
        create_vendor,
        listing_repository,
        create_listing_request,
    ):
        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_vendor.id, dto)

        listing = await listing_repository.get_by_id(listing_id)
        change_description_dto = ChangeListingDescriptionRequest(
            description="Новое описание"
        )
        await change_listing_description_usecase.execute(
            create_vendor.id, listing_id, change_description_dto
        )

        listing_after = await listing_repository.get_by_id(listing_id)
        assert listing_after.description != listing.description
