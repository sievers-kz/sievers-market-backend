from uuid import UUID

from src.core.shared.domain.enums import PriceCurrency
from src.core.shared.presentation.dto import DTO


class AttributeResponse(DTO):
    base_fields: list[dict]
    dynamic_fields: list[dict]


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


class ListingCardResponse(DTO):
    id: UUID
    last_name: str
    first_name: str
    subcategory: str
    title: str
    price: int
    currency: str
    city: str
    preview_image: UUID

