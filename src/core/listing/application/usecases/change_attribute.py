from uuid import UUID

from loguru import logger

from src.core.catalog.application.services.subcategory import SubcategoryService
from src.core.listing.application.interfaces.uow import IListingUnitOfWork
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.presentation.dto import ChangeListingAttributeRequest


class ChangeListingAttributeUseCase:
    def __init__(
        self, uow: IListingUnitOfWork, subcategory_service: SubcategoryService
    ):
        self.uow = uow
        self.subcategory_service = subcategory_service

    async def execute(
        self, vendor_id: UUID, listing_id: UUID, dto: ChangeListingAttributeRequest
    ):
        validated_attributes = await self.subcategory_service.validate_attributes(
            dto.subcategory_id, dto.attributes
        )

        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing:
                raise ListingNotFoundError()

            listing.change_attributes(validated_attributes)
            await uow.listing.save(listing)
            await uow.commit()

        logger.info("Listing attributes changed | listing_id={}", listing.id)
