from uuid import UUID

from src.api.listings.dto import CreateActiveListingDTO
from src.core.listings.application.specification_validation import validate_specification_fields
from src.core.listings.infrastructure.factories import ListingFactory
from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class CreateListingUseCase:
    def __init__(self, unit_of_work: AbstractListingReferenceUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, listing_dto: CreateActiveListingDTO, user_id: UUID):
        subcategory_id = listing_dto.machinery.subcategory_id
        extra_specifications = listing_dto.machinery.extra_specs

        async with self.unit_of_work as uow:
            specification_references = await uow.reference.get_subcategory_specifications(subcategory_id)
            validate_specification_fields(extra_specifications, specification_references)

            listing = ListingFactory.create(listing_dto, user_id)
            listing.publish()

            await uow.listing.save(listing)
            await uow.commit()

