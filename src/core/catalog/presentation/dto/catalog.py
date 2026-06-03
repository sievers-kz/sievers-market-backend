from uuid import UUID

from typing import Any

from pydantic import field_validator

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


class ListingDetailResponse(DTO):
    id: UUID
    owner_id: UUID
    email: str
    phone: str | None
    last_name: str
    first_name: str
    subcategory: str
    title: str
    price: int
    currency: str
    city: str
    description: str | None
    gallery: list[UUID]
    attributes: dict[str, Any]

    @field_validator("gallery", mode="before")
    @classmethod
    def extract_media_ids(cls, v):
        return [item["media_id"] for item in v]


class VendorCardResponse(DTO):
    vendor_id: UUID
    is_verified: bool
    legal_name: str
    shop_name: str | None
    logotype: dict | None
