import uuid
from uuid import UUID

from src.core.catalog.application.services.subcategory import SubcategoryService
from src.core.listing.application.interfaces.uow import IListingUnitOfWork
from src.core.listing.domain.entities import Listing
from src.core.listing.domain.value_objects import Gallery
from src.core.listing.presentation.dto import CreateListingRequest
from src.core.listing.domain.enums import ListingStatus


class CreateListingUseCase:
    def __init__(
        self,
        uow: IListingUnitOfWork,
        subcategory_service: SubcategoryService,
    ):
        self.uow = uow
        self.subcategory_service = subcategory_service

    async def execute(self, owner_id: UUID, dto: CreateListingRequest):
        validated_attributes = await self.subcategory_service.validate_attributes(dto.subcategory_id, dto.attributes)

        async with self.uow as uow:
            listing = Listing(
                id=uuid.uuid4(),
                owner_id=owner_id,
                category_id=dto.category_id,
                subcategory_id=dto.subcategory_id,
                title=dto.title,
                price=dto.price,
                currency=dto.currency,
                city_id=dto.city_id,
                description=dto.description,
                attributes=validated_attributes,
                gallery=Gallery.from_dicts([item.model_dump() for item in dto.gallery]),
                status=ListingStatus.ACTIVE,
            )

            await uow.listing.save(listing)
            await uow.commit()



