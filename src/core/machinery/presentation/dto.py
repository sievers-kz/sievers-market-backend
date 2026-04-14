from typing import Any
from uuid import UUID

from pydantic import Field

from src.core.shared.presentation.dto import DTO
from src.core.machinery.domain.enums import MachineryCondition
from src.core.shared.domain.enums import PriceCurrency


class CreateMachineryRequest(DTO):
    subcategory_id: UUID
    price: int
    currency: PriceCurrency
    city_id: UUID
    description: str | None = None
    brand_id: UUID
    model: str | None = None
    year_of_issue: int
    condition: MachineryCondition
    color_id: UUID | None = None
    country_id: UUID | None = None

    attributes: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {
                "engine_power": 620,
                "max_speed": 120,
                "weight": 3000
            }
        },
        description="Динамические характеристики техники"
    )


class MachineryCardQuery(DTO):
    id: UUID
    title: str
    price: int
    currency: PriceCurrency
    subcategory: str
    city: str


class PaginatedMachinery(DTO):
    items: list[MachineryCardQuery]
    total: int
    page: int
    limit: int
    pages_count: int


class MachineryOwner(DTO):
    id: UUID
    last_name: str
    first_name: str
    phone: str | None = None


class MachineryDetailQuery(DTO):
    id: UUID
    subcategory: str
    title: str
    price: int
    currency: PriceCurrency
    city: str
    description: str | None
    brand: str
    model: str | None
    year_of_issue: int
    condition: MachineryCondition
    color: str | None
    country: str | None
    customer: MachineryOwner

    attributes: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {
                "engine_power": 620,
                "max_speed": 120,
                "weight": 3000
            }
        }
    )


class MachineryOwnerDetailQuery(DTO):
    id: UUID
    subcategory: str
    title: str
    price: int
    currency: PriceCurrency
    city: str
    description: str | None
    brand: str
    model: str | None
    year_of_issue: int
    condition: MachineryCondition
    color: str | None
    country: str | None
    customer: MachineryOwner
    wishlist_total_count: int = Field(default=0)

    attributes: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {
                "engine_power": 620,
                "max_speed": 120,
                "weight": 3000
            }
        }
    )


class ChangeMachineryCategoryRequest(DTO):
    subcategory_id: UUID


class ChangeMachineryGeneralRequest(DTO):
    brand_id: UUID
    model: str | None = None
    color_id: UUID | None = None
    country_id: UUID | None = None


class ChangeOperatingHistoryRequest(DTO):
    year_of_issue: int
    condition: MachineryCondition


class ChangeMachineryPriceRequest(DTO):
    price: int
    currency: PriceCurrency


class ChangeMachinerySpecRequest(DTO):
    subcategory_id: UUID
    attributes: dict[str, Any] | None = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {
                "engine_power": 620,
                "max_speed": 120,
                "weight": 3000
            }
        },
        description="Динамические характеристики техники"
    )


class ChangeMachineryDescriptionRequest(DTO):
    description: str | None

