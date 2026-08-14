from typing import Any
from uuid import UUID

from pydantic import ConfigDict, Field

from src.core.listing.domain.entities import Listing
from src.core.listing.domain.enums import ListingStatus
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


class ListingSearchDocument(DTO):
    id: str
    title: str
    price: int
    currency: str
    city_id: str
    subcategory_id: str
    is_active: bool
    model_config = ConfigDict(extra="allow")

    @classmethod
    def from_listing(
        cls, listing: Listing, attributes: dict
    ) -> "ListingSearchDocument":
        return cls.model_validate(
            {
                "id": str(listing.id),
                "title": listing.title,
                "price": listing.price,
                "currency": listing.currency,
                "city_id": str(listing.city_id),
                "subcategory_id": str(listing.subcategory_id),
                "is_active": listing.status == ListingStatus.ACTIVE,
                **attributes,
            }
        )


class ListingSearchQuery(DTO):
    text: str | None = None
    subcategory_id: str | None = None
    city_id: str | None = None
    price_min: int | None = None
    price_max: int | None = None
    attributes: dict[str, Any] = {}
    page: int = 1
    limit: int = 20
