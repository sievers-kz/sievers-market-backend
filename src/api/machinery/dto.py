from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.core.machinery.domain.enums import PriceCurrency, MachineryCondition, ListingStatus


class CreateMachinery(BaseModel):
    subcategory_id: UUID
    title: str
    price: int
    currency: PriceCurrency
    city_id: UUID
    description: str | None
    brand_id: UUID
    model: str | None
    year_of_issue: int
    condition: MachineryCondition
    color_id: UUID | None
    attributes: dict
    country_id: UUID | None


class UpdateMachinery(BaseModel):
    subcategory_id: UUID
    title: str
    price: int
    currency: PriceCurrency
    city_id: UUID
    description: str | None
    brand_id: UUID
    model: str | None
    year_of_issue: int
    condition: MachineryCondition
    color_id: UUID | None
    attributes: dict
    country_id: UUID | None


class MachineryCard(BaseModel):
    id: UUID
    title: str
    subcategory: str
    price: int
    currency: PriceCurrency
    city: str
    created_at: datetime


class MachineryOwnerCard(BaseModel):
    id: UUID
    title: str
    subcategory: str
    price: int
    currency: PriceCurrency
    city: str
    views: int = 0
    status: ListingStatus
    created_at: datetime


class PaginatedMachinery(BaseModel):
    items: list
    total: int
    page: int
    limit: int
    pages_count: int


class SellerInfo(BaseModel):
    id: UUID
    company_name: str
    phone: str


class DetailMachinery(BaseModel):
    id: UUID
    seller: SellerInfo
    title: str
    subcategory: str
    price: int
    currency: PriceCurrency
    city: str
    description: str | None
    brand: str
    model: str | None
    year_of_issue: int
    condition: MachineryCondition
    color: str | None
    attributes: dict
    country: str | None


class OwnerDetailMachinery(BaseModel):
    id: UUID
    seller: SellerInfo
    title: str
    subcategory: str
    price: int
    currency: PriceCurrency
    city: str
    description: str | None
    brand: str
    model: str | None
    year_of_issue: int
    condition: MachineryCondition
    color: str | None
    attributes: dict
    country: str | None
    status: ListingStatus
    views: int = 0
    created_at: datetime
