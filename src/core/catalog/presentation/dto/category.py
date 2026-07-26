from uuid import UUID

from src.core.shared.presentation.dto import DTO


class CreateCategoryRequest(DTO):
    rubric_id: UUID
    name: str


class ChangeCategoryParentRequest(DTO):
    rubric_id: UUID


class ChangeCategoryNameRequest(DTO):
    name: str


class CategoryResponse(DTO):
    id: UUID
    rubric_id: UUID
    name: str
