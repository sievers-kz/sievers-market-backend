from uuid import UUID

from src.core.catalog.domain.enums import AttributeType
from src.core.shared.presentation.dto import DTO


class Attribute(DTO):
    key: str
    label: str
    type: AttributeType
    required: bool = False
    filterable: bool = False
    unit: dict[str, str] | str | None = None
    options: list[dict[str, str]] | list[str] | None = None
    source: str | None = None
    position: int = 0


class CreateSubcategoryRequest(DTO):
    category_id: UUID
    name: str
    attributes: list[Attribute]


class ChangeSubcategoryParentRequest(DTO):
    category_id: UUID


class ChangeSubcategoryNameRequest(DTO):
    name: str


class ReplaceSubcategoryAttributeRequest(DTO):
    attributes: list[Attribute]
