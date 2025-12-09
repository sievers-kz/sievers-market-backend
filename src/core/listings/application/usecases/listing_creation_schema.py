from uuid import UUID

from src.api.listings.dto import FormSchemaResponse
from src.api.references.dto import AllReferencesDTO, SpecificationDTO
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.listings.infrastructure.form_builder import ListingFormBuilderService
from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class GetListingCreationSchemaUseCase:
    def __init__(
        self,
        unit_of_work: AbstractListingReferenceUnitOfWork,
        token_service: AbstractTokenService,
        form_builder: ListingFormBuilderService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.form_builder = form_builder

    async def execute(self, subcategory_id: UUID):
        async with self.unit_of_work as uow:
            references: AllReferencesDTO = await uow.reference.get_common_lookups()
            specifications: SpecificationDTO = await uow.reference.get_subcategory_specifications(subcategory_id)

            schema = self.form_builder.build_form_schema(specifications)
            return FormSchemaResponse(subcategory_id=subcategory_id, schema=schema, references=references)
