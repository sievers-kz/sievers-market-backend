from uuid import UUID

from src.core.references.application.interfaces.abstract_attribute_repository import AbstractAttributeRepository
from src.core.references.infrastructure.filter_builder import FilterBuilderService


class GetSubcategoryFilterUseCase:
    def __init__(self, repository: AbstractAttributeRepository, filter_builder: FilterBuilderService):
        self.repository = repository
        self.filter_builder = filter_builder

    async def execute(self, subcategory_id: UUID):
        attributes = await self.repository.get_by_subcategory_id(subcategory_id)
        if not attributes:
            return None

        filters = self.filter_builder.build(attributes) # <- Возвращает подготовленный под Flutter список
        return filters                                  # объектов Pydantic для построения фильтров
