from uuid import UUID

from loguru import logger

from src.core.listing.application.interfaces.uow import IListingUnitOfWork
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.presentation.dto import ChangeListingLocationRequest


class ChangeListingLocationUseCase:
    def __init__(self, uow: IListingUnitOfWork):
        self.uow = uow

    async def execute(self, listing_id: UUID, dto: ChangeListingLocationRequest):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing:
                raise ListingNotFoundError()

            listing.change_location(dto.city_id)
            await uow.listing.save(listing)
            await uow.commit()

        logger.info("Listing location changed | listing_id={} new_location={}", listing.id, listing.city_id)
