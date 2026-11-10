from uuid import UUID

from loguru import logger

from src.core.catalog.infrastructure.attribute_validation import (
    AttributeValidationService,
)
from src.core.customer.application.services.organization_service import OrganizationService
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.uow import ListingUnitOfWork
from src.core.listing.presentation.dto import ChangeListingAttributeRequest


class ChangeListingAttributeUseCase:
    def __init__(
        self,
        uow: ListingUnitOfWork,
        attribute_validation: AttributeValidationService,
        organization_service: OrganizationService,
    ):
        self.uow = uow
        self.attribute_validation = attribute_validation
        self.organization_service = organization_service

    async def execute(self, customer_id: UUID, listing_id: UUID, dto: ChangeListingAttributeRequest):
        validated_attributes = await self.attribute_validation.validate(dto.subcategory_id, dto.attributes)

        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or not await self.organization_service.is_owner(customer_id, listing.organization_id):
                raise ListingNotFoundError()

            listing.change_attributes(listing.organization_id, validated_attributes)
            await uow.listing.save(listing)
            await uow.commit()

        logger.info("Listing attributes changed | listing_id={}", listing.id)
