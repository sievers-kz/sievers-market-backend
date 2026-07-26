from uuid import UUID

from src.core.shared.presentation.dto import DTO


class CreateSubcategoryRequest(DTO):
    category_id: UUID
    name: str


class ChangeSubcategoryParentRequest(DTO):
    category_id: UUID


class ChangeSubcategoryNameRequest(DTO):
    name: str


class SubcategoryResponse(DTO):
    id: UUID
    category_id: UUID
    name: str
