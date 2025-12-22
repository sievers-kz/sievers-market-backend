from uuid import UUID

from src.api.listings.dto import UpdateListingFormSchemaDTO
from src.core.listings.application.abstract_listing_query_context import AbstractListingQueryContext
from src.core.listings.infrastructure.form_builder import ListingFormBuilderService
from src.core.references.application.abstract_reference_query_context import AbstractReferenceQueryContext


class UpdateListingSchemaUseCase:
    def __init__(
        self,
        listing_query_service: AbstractListingQueryContext,
        reference_query_service: AbstractReferenceQueryContext,
        form_builder: ListingFormBuilderService
    ):
        self.listing_query_service = listing_query_service
        self.reference_query_service = reference_query_service
        self.form_builder = form_builder

    async def execute(self, listing_id: UUID):
        async with self.listing_query_service as query:
            listing = await query.listing.get_listing_by_id(listing_id)
            subcategory_id = listing.machinery.subcategory_id

        async with self.reference_query_service as query:
            common_references = await query.reference.get_common_lookups()
            specifications = await query.specification.get_subcategory_specifications(subcategory_id)

        form_schema = self.form_builder.build_form_schema(specifications)

        return UpdateListingFormSchemaDTO(
            listing_id=listing_id,
            form_schema=form_schema,
            initial_listing_data=listing,
            references=common_references
        )
