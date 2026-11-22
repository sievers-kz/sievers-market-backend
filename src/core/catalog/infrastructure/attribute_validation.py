from uuid import UUID

from pydantic import Field
from pydantic import ValidationError as PydanticValidationError
from pydantic import create_model

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.catalog.infrastructure.repositories.attributes import (
    SubcategoryAttributeRepository,
)
from src.core.catalog.infrastructure.repositories.categories import (
    SubcategoryRepository,
)


class AttributeValidationService:
    def __init__(
        self,
        link_repo: SubcategoryAttributeRepository,
        subcategory_repo: SubcategoryRepository,
    ):
        self._link_repo = link_repo
        self._subcategory_repo = subcategory_repo

    async def validate(self, subcategory_id: UUID, raw_attributes: dict) -> dict:
        # Подкатегория без атрибутов допустима: пустой набор характеристик не ошибка.
        # Отсутствие самой подкатегории проверяем отдельно.
        if await self._subcategory_repo.get_by_id(subcategory_id) is None:
            raise CatalogNotFoundError(field=str(subcategory_id))

        links = await self._link_repo.get_with_definitions(subcategory_id)

        fields = {}
        for link in links:
            py_type = self._map_type(link.attribute.type)
            fields[link.attribute.key] = (
                (py_type, Field(...)) if link.required else (py_type | None, Field(default=None))
            )

        dynamic_model = create_model(f"Subcategory_{subcategory_id}_Model", **fields)

        try:
            validated = dynamic_model(**raw_attributes)
            return validated.model_dump()
        except PydanticValidationError as e:
            raise PydanticValidationError.from_exception_data(e.title, e.errors()) from e

    @staticmethod
    def _map_type(attr_type: AttributeType):
        mapping = {
            AttributeType.INTEGER: int,
            AttributeType.FLOAT: float,
            AttributeType.BOOLEAN: bool,
            AttributeType.ENUMERATE: str,
            AttributeType.STRING: str,
        }
        return mapping.get(attr_type, str)
