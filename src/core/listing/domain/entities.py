from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.core.listing.domain.value_objects import Gallery
from src.core.shared.domain.entities import AggregateRoot
from src.core.shared.domain.enums import PriceCurrency
from src.core.listing.domain.enums import ListingStatus


@dataclass(frozen=False)
class Listing(AggregateRoot):
    id: UUID
    owner_id: UUID
    category_id: UUID
    subcategory_id: UUID
    title: str
    price: int
    currency: PriceCurrency
    city_id: UUID
    description: str | None
    attributes: dict[str, Any]
    gallery: Gallery
    status: ListingStatus

    def change_price(self, new_price: int, new_currency: PriceCurrency) -> None:
        self.price = new_price
        self.currency = new_currency

    def change_location(self, city_id: UUID) -> None:
        self.city_id = city_id

    def change_description(self, description: str) -> None:
        self.description = description
        
    def change_attributes(self, attributes: dict[str, Any]) -> None:
        self.attributes = attributes



