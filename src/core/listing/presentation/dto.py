import math
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import ConfigDict, Field, field_validator, model_validator

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
    organization_id: UUID
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
        json_schema_extra={"example": {"engine_power": 300, "max_speed": 60, "weight": 4000}},
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
    category_id: str
    subcategory_id: str
    is_active: bool
    description: str | None = None
    # Unix-время в секундах: число сортируется в Meilisearch надёжнее строки с датой.
    created_at: int | None = None
    model_config = ConfigDict(extra="allow")

    @classmethod
    def from_listing(cls, listing: Listing, attributes: dict) -> "ListingSearchDocument":
        return cls.model_validate(
            {
                "id": str(listing.id),
                "title": listing.title,
                "price": listing.price,
                "currency": listing.currency,
                "city_id": str(listing.city_id),
                "category_id": str(listing.category_id),
                "subcategory_id": str(listing.subcategory_id),
                "is_active": listing.status == ListingStatus.ACTIVE,
                "description": listing.description,
                "created_at": int(listing.created_at.timestamp()) if listing.created_at else None,
                **attributes,
            }
        )


class ListingSearchSort(str, Enum):
    NEWEST = "newest"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"


class NumericRange(DTO):
    """Диапазон для числового атрибута; можно задать одну границу."""

    min: float | None = None
    max: float | None = None

    @model_validator(mode="after")
    def check_bounds(self) -> "NumericRange":
        if self.min is None and self.max is None:
            raise ValueError("Задайте хотя бы одну границу диапазона")
        for bound in (self.min, self.max):
            if bound is not None and not math.isfinite(bound):
                raise ValueError("Границы диапазона должны быть конечными числами")
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("Нижняя граница больше верхней")
        return self


class ListingSearchQuery(DTO):
    text: str | None = None
    category_id: UUID | None = None
    subcategory_id: UUID | None = None
    city_id: UUID | None = None
    price_min: int | None = Field(None, ge=0)
    price_max: int | None = Field(None, ge=0)
    # Ключи атрибутов допустимы только вместе с `subcategory_id`: фильтруемые атрибуты задаются подкатегорией.
    attributes: dict[str, str | int | float | bool] = {}
    # Диапазоны «от–до» для числовых атрибутов (`integer`, `float`), тоже только вместе с `subcategory_id`.
    attribute_ranges: dict[str, NumericRange] = {}
    # Без `sort`: при тексте порядок по релевантности, без текста сначала новые.
    sort: ListingSearchSort | None = None
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=50)

    @field_validator("attributes")
    @classmethod
    def reject_non_finite_numbers(cls, value: dict[str, str | int | float | bool]):
        # NaN и Infinity не имеют записи в выражении фильтра Meilisearch.
        for key, item in value.items():
            if isinstance(item, float) and not math.isfinite(item):
                raise ValueError(f"Значение атрибута {key} должно быть конечным числом")
        return value


class ListingCardResponse(DTO):
    id: UUID
    subcategory: str
    title: str
    price: int
    currency: str
    city: str
    preview_image: UUID
    created_at: datetime
    organization_name: str | None = None
    condition: str | None = None


class MyListingsStatus(str, Enum):
    """Статусы, доступные в фильтре «Мои объявления». Удалённые объявления владельцу не показываются."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class MyListingsSort(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"


class MyListingCardResponse(DTO):
    id: UUID
    title: str | None
    price: int | None
    currency: str | None
    status: ListingStatus
    category: str
    subcategory: str
    organization_id: UUID
    organization_name: str | None
    city: str | None
    preview_image: UUID | None
    created_at: datetime


class ListingSpecItem(DTO):
    """Характеристика, готовая к показу.

    `value`: подпись варианта, название из справочника, «Да»/«Нет» или число как есть
    (число форматирует фронт, единица измерения отдельно в `unit`).
    """

    key: str
    label: str
    value: str | int | float
    unit: str | None


class ListingSpecGroup(DTO):
    key: str
    label: str
    items: list[ListingSpecItem]


class ListingSeller(DTO):
    """Продавец: организация, от имени которой подано объявление. Контакты публичные."""

    organization_id: UUID
    name: str | None
    phone: str | None
    email: str | None
    logo_media_id: UUID | None


class ListingDetailResponse(DTO):
    id: UUID
    # Это id организации, а не пользователя; оставлено для совместимости, то же значение в `seller.organization_id`.
    owner_id: UUID
    category_id: UUID
    category: str
    subcategory_id: UUID
    subcategory: str
    title: str
    price: int
    currency: str
    city: str
    description: str | None
    gallery: list[UUID]
    attributes: dict[str, Any]
    condition: str | None
    created_at: datetime
    seller: ListingSeller
    specs: list[ListingSpecGroup]

    @field_validator("gallery", mode="before")
    @classmethod
    def extract_media_ids(cls, v):
        return [item["media_id"] for item in v]
