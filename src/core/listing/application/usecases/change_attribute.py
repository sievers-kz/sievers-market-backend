from uuid import UUID

from loguru import logger

from src.core.catalog.infrastructure.attribute_validation import (
    AttributeValidationService,
)
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.customer.application.services.organization_service import OrganizationService
from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.uow import ListingUnitOfWork
from src.core.listing.presentation.dto import ChangeListingAttributeRequest


class ChangeListingAttributeUseCase:
    def __init__(
        self,
        uow: ListingUnitOfWork,
        attribute_validation: AttributeValidationService,
        listing_search_service: ListingSearchService,
        organization_service: OrganizationService,
    ):
        self.uow = uow
        self.attribute_validation = attribute_validation
        self.listing_search_service = listing_search_service
        self.organization_service = organization_service

    async def execute(self, customer_id: UUID, listing_id: UUID, dto: ChangeListingAttributeRequest):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or not await self.organization_service.is_owner(customer_id, listing.organization_id):
                raise ListingNotFoundError()

            # Характеристики проверяются по схеме подкатегории самого объявления, а не любой присланной.
            if dto.subcategory_id != listing.subcategory_id:
                raise CatalogNotFoundError(field=str(dto.subcategory_id))

            validated_attributes = await self.attribute_validation.validate(dto.subcategory_id, dto.attributes)

            listing.change_attributes(listing.organization_id, validated_attributes)
            await uow.listing.save(listing)
            await uow.commit()

        await self.listing_search_service.sync_listing(listing)

        logger.info("Listing attributes changed | listing_id={}", listing.id)
