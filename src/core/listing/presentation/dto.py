from typing import Any
from uuid import UUID

from pydantic import Field

from src.core.shared.domain.enums import PriceCurrency
from src.core.shared.presentation.dto import DTO


class ListingImage(DTO):
    # TODO: Добавить дополнительные метаданные
    # type
    # size_bytes
    media_id: UUID
    media_type: str
    media_size: int


class CreateListingRequest(DTO):
    category_id: UUID
    subcategory_id: UUID
    title: str
    price: int
    currency: PriceCurrency
    city_id: UUID
    description: str | None
    gallery: list[ListingImage]

    attributes: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {"engine_power": 300, "max_speed": 60, "weight": 4000}
        },
        description="Динамические спецификации объявления",
    )


class ChangeListingPriceRequest(DTO):
    price: int
    currency: PriceCurrency


class ChangeListingLocationRequest(DTO):
    city_id: UUID


class ChangeListingDescriptionRequest(DTO):
    description: str


class ChangeListingAttributeRequest(DTO):
    subcategory_id: UUID
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {
                "width": 1200,
                "height": 1400,
                "length": 1600,
            }
        },
    )
