from uuid import UUID

from typing import Any

from pydantic import field_validator

from src.core.shared.domain.enums import PriceCurrency
from src.core.shared.presentation.dto import DTO
from src.core.vendor.domain.enums import LegalForm


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
    display_owner_name: str
    subcategory: str
    title: str
    price: int
    currency: str
    city: str
    preview_image: UUID


class ListingDetailResponse(DTO):
    id: UUID
    owner_id: UUID
    contact_phone: str | None
    display_owner_name: str
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
    display_name: str
    logotype: dict | None


class DetailVendorResponse(DTO):
    id: UUID
    contact_phone: str | None
    legal_name: str
    legal_address: str
    tax_id: str
    legal_form: LegalForm
    shop_name: str | None
    logotype: dict | None
    is_verified: bool

