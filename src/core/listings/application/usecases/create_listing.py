from uuid import UUID

from src.api.listings.dto import CreateActiveListingDTO
from src.core.listings.application.abstract_listing_unit_of_work import AbstractListingUnitOfWork
from src.core.listings.application.specification_validation import validate_specification_fields
from src.core.listings.infrastructure.factories import ListingFactory
from src.core.references.application.abstract_reference_query_context import AbstractReferenceQueryContext


class CreateListingUseCase:
    def __init__(
        self,
        unit_of_work: AbstractListingUnitOfWork,
        query_service: AbstractReferenceQueryContext
    ):
        self.unit_of_work = unit_of_work
        self.query_service = query_service

    async def execute(self, listing_dto: CreateActiveListingDTO, user_id: UUID):
        subcategory_id = listing_dto.machinery.subcategory_id
        async with self.query_service as query:
            specifications_references = await query.specification.get_subcategory_specifications(subcategory_id)

        extra_specs = listing_dto.machinery.extra_specs
        validate_specification_fields(extra_specs, specifications_references)

        async with self.unit_of_work as uow:
            listing = ListingFactory.create(listing_dto, user_id)
            listing.publish()

            await uow.listing.save(listing)
            await uow.commit()

