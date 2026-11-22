import uuid

import pytest

from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError


class TestCreateListingUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_listing_success(
        self,
        create_listing_usecase,
        listing_repository,
        create_organization,
        create_listing_request,
    ):
        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_organization.owner_id, dto)

        listing = await listing_repository.get_by_id(listing_id)
        assert listing is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_listing_rejects_unknown_category(
        self,
        create_listing_usecase,
        create_organization,
        create_listing_request,
    ):
        dto = create_listing_request.model_copy(update={"category_id": uuid.uuid4()})

        with pytest.raises(CatalogNotFoundError):
            await create_listing_usecase.execute(create_organization.owner_id, dto)
