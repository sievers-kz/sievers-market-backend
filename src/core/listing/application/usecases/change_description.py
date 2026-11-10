from uuid import UUID

from loguru import logger

from src.core.customer.application.services.organization_service import OrganizationService
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.uow import ListingUnitOfWork
from src.core.listing.presentation.dto import ChangeListingDescriptionRequest


class ChangeListingDescriptionUseCase:
    def __init__(self, uow: ListingUnitOfWork, organization_service: OrganizationService):
        self.uow = uow
        self.organization_service = organization_service

    async def execute(self, customer_id: UUID, listing_id: UUID, dto: ChangeListingDescriptionRequest):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or not await self.organization_service.is_owner(customer_id, listing.organization_id):
                raise ListingNotFoundError()

            listing.change_description(listing.organization_id, dto.description)
            await uow.listing.save(listing)
            await uow.commit()

        logger.info("Listing description changed | listing_id={}", listing.id)
