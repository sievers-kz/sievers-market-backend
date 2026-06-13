import uuid

import pytest

from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.presentation.dto import ChangeListingPriceRequest
from src.core.shared.domain.enums import PriceCurrency


class TestChangeListingPriceUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_listing_price_success(
        self,
        create_listing_usecase,
        change_listing_price_usecase,
        create_vendor,
        listing_repository,
        create_listing_request,
    ):
        dto = create_listing_request
        listing_id = await create_listing_usecase.execute(create_vendor.id, dto)

        listing = await listing_repository.get_by_id(listing_id)
        change_price_dto = ChangeListingPriceRequest(
            price="100", currency=PriceCurrency.USD
        )
        await change_listing_price_usecase.execute(
            create_vendor.id, listing_id, change_price_dto
        )

        listing_after = await listing_repository.get_by_id(listing_id)
        assert listing_after.price != listing.price

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_listing_price_when_listing_not_found(
        self,
        create_listing_usecase,
        change_listing_price_usecase,
        create_vendor,
        listing_repository,
        create_listing_request,
    ):
        listing_id = uuid.uuid4()
        dto = ChangeListingPriceRequest(price="100", currency=PriceCurrency.USD)

        with pytest.raises(ListingNotFoundError):
            await change_listing_price_usecase.execute(
                create_vendor.id, listing_id, dto
            )
