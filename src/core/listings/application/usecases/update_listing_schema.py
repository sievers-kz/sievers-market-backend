from uuid import UUID

from src.api.listings.dto import UpdateListingFormSchemaDTO, InitialListingDataDTO
from src.api.references.dto import AllReferencesDTO, SpecificationDTO
from src.core.listings.infrastructure.form_builder import ListingFormBuilderService
from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class UpdateListingSchemaUseCase:
    def __init__(
        self,
        unit_of_work: AbstractListingReferenceUnitOfWork,
        form_builder: ListingFormBuilderService
    ):
        self.unit_of_work = unit_of_work
        self.form_builder = form_builder

    async def execute(self, listing_id: UUID):
        async with self.unit_of_work as uow:
            listing = await uow.listing.get_listing_by_id(listing_id)
            subcategory_id = listing.machinery.subcategory_id

            references: AllReferencesDTO = await uow.reference.get_common_lookups()
            specifications: SpecificationDTO = await uow.reference.get_subcategory_specifications(subcategory_id)
            form_schema = self.form_builder.build_form_schema(specifications)
            initial_data = InitialListingDataDTO.model_validate(listing, from_attributes=True)

            return UpdateListingFormSchemaDTO(
                listing_id=listing_id,
                form_schema=form_schema,
                initial_listing_data=initial_data,
                references=references
            )
