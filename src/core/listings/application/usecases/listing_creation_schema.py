from uuid import UUID

from src.api.listings.dto import FormSchemaResponse
from src.core.listings.infrastructure.form_builder import ListingFormBuilderService
from src.core.references.application.abstract_reference_query_context import AbstractReferenceQueryContext


class GetListingCreationSchemaUseCase:
    def __init__(
        self,
        query_service: AbstractReferenceQueryContext,
        form_builder: ListingFormBuilderService
    ):
        self.query_service = query_service
        self.form_builder = form_builder

    async def execute(self, subcategory_id: UUID):
        async with self.query_service as query:
            references = await query.reference.get_common_lookups()
            specifications = await query.specification.get_subcategory_specifications(subcategory_id)
            schema = self.form_builder.build_form_schema(specifications)
            return FormSchemaResponse(subcategory_id=subcategory_id, schema=schema, references=references)
