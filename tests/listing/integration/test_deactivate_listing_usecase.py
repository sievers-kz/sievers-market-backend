import pytest

from src.core.listing.domain.enums import ListingStatus


class TestDeactivateListingUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_deactivate_listing_success(
        self,
        create_listing_usecase,
        deactivate_listing_usecase,
        create_vendor,
        listing_repository,
        create_listing_request,
    ):
        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_vendor.id, dto)

        await deactivate_listing_usecase.execute(create_vendor.id, listing_id)
        listing = await listing_repository.get_by_id(listing_id)

        assert listing is not None
        assert listing.status == ListingStatus.INACTIVE
