from uuid import UUID

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.shared.presentation.dto import DTO


class AttributeFieldResponse(DTO):
    key: str
    label: str
    type: AttributeType
    required: bool
    filterable: bool
    unit: dict | None
    options: list[dict]
    source: str | None = None


class AttributeGroupFieldsResponse(DTO):
    key: str
    label: str
    position: int
    fields: list[AttributeFieldResponse]


class AttributeResponse(DTO):
    groups: list[AttributeGroupFieldsResponse]


class FilterableAttributeResponse(DTO):
    filters: list[AttributeFieldResponse]


class SubcategoryResponse(DTO):
    id: UUID
    category_id: UUID
    name: str


class CategoryResponse(DTO):
    id: UUID
    rubric_id: UUID
    name: str
    subcategories: list[SubcategoryResponse]


class RubricResponse(DTO):
    id: UUID
    name: str
    categories: list[CategoryResponse]
