from uuid import UUID

from loguru import logger

from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.uow import ListingUnitOfWork
from src.core.listing.presentation.dto import ChangeListingDescriptionRequest


class ChangeListingDescriptionUseCase:
    def __init__(self, uow: ListingUnitOfWork):
        self.uow = uow

    async def execute(self, organization_id: UUID, listing_id: UUID, dto: ChangeListingDescriptionRequest):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or listing.organization_id != organization_id:
                raise ListingNotFoundError()

            listing.change_description(organization_id, dto.description)
            await uow.listing.save(listing)
            await uow.commit()

        logger.info("Listing description changed | listing_id={}", listing.id)
