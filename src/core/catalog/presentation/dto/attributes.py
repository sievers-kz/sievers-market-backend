from uuid import UUID

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.shared.presentation.dto import DTO


class OptionItem(DTO):
    key: str
    label: str


class CreateAttributeDefinitionRequest(DTO):
    key: str
    label: str
    type: AttributeType
    options: list[OptionItem] = []
    source: str | None = None


class AttributeDefinitionResponse(DTO):
    id: UUID
    key: str
    label: str
    type: AttributeType
    options: list[OptionItem]
    source: str | None = None


class CreateAttributeGroupRequest(DTO):
    key: str
    label: str
    position: int = 0


class AttributeGroupResponse(DTO):
    id: UUID
    key: str
    label: str
    position: int


class CreateUnitOfMeasureRequest(DTO):
    key: str
    label: str


class UnitOfMeasureResponse(DTO):
    id: UUID
    key: str
    label: str


class AttachAttributeRequest(DTO):
    attribute_id: UUID
    group_id: UUID
    unit_id: UUID | None = None
    required: bool = False
    filterable: bool = False
    position: int = 0


class SubcategoryAttributeResponse(DTO):
    id: UUID
    subcategory_id: UUID
    attribute_id: UUID
    group_id: UUID
    unit_id: UUID | None
    required: bool
    filterable: bool
    position: int
