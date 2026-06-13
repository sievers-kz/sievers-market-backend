import pytest


class TestCreateListingUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_listing_success(
        self,
        create_listing_usecase,
        listing_repository,
        create_vendor,
        create_listing_request,
    ):
        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_vendor.id, dto)

        listing = await listing_repository.get_by_id(listing_id)
        assert listing is not None
