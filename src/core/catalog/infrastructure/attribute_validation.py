from uuid import UUID

from pydantic import Field
from pydantic import ValidationError as PydanticValidationError
from pydantic import create_model

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.catalog.infrastructure.repositories.attributes import (
    SubcategoryAttributeRepository,
)


class AttributeValidationService:
    def __init__(
        self,
        link_repo: SubcategoryAttributeRepository,
    ):
        self._link_repo = link_repo

    async def validate(self, subcategory_id: UUID, raw_attributes: dict) -> dict:
        links = await self._link_repo.get_with_definitions(subcategory_id)
        if not links:
            raise CatalogNotFoundError(field=str(subcategory_id))

        fields = {}
        for link in links:
            py_type = self._map_type(link.attribute.type)
            fields[link.attribute.key] = (
                (py_type, Field(...))
                if link.required
                else (py_type | None, Field(default=None))
            )

        dynamic_model = create_model(f"Subcategory_{subcategory_id}_Model", **fields)

        try:
            validated = dynamic_model(**raw_attributes)
            return validated.model_dump()
        except PydanticValidationError as e:
            raise PydanticValidationError.from_exception_data(
                e.title, e.errors()
            ) from e

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
