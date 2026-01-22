from uuid import UUID

from src.core.references.application.interfaces.abstract_attribute_repository import AbstractAttributeRepository
from src.core.references.application.interfaces.abstract_subcategory_repository import AbstractSubcategoryRepository
from src.core.references.infrastructure.form_builder import FormBuilderService


class GetSubcategoryFormUseCase:
    def __init__(
        self,
        subcategory_repository: AbstractSubcategoryRepository,
        attribute_repository: AbstractAttributeRepository,
        form_builder: FormBuilderService
    ):
        self.subcategory_repository = subcategory_repository
        self.attribute_repository = attribute_repository
        self.form_builder = form_builder

    async def execute(self, subcategory_id: UUID):
        subcategory = await self.subcategory_repository.get_rubric_by_subcategory(subcategory_id)
        if not subcategory:
            raise ValueError("Subcategory not found")

        rubric_name = subcategory.category.rubric.name
        attributes = await self.attribute_repository.get_by_subcategory_id(subcategory_id)

        form = self.form_builder.build(rubric=rubric_name, attributes=attributes)
        return form
