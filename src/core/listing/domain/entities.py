from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.core.listing.domain.exceptions import ListingActivationError, ListingArchivingError
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

    def activate(self):
        if self.status == ListingStatus.DELETED:
            raise ListingActivationError()
        if self.status == ListingStatus.ACTIVE:
            return
        self.status = ListingStatus.ACTIVE

    def deactivate(self):
        if self.status == ListingStatus.INACTIVE:
            return
        self.status = ListingStatus.INACTIVE

    def archive(self):
        if self.status == ListingStatus.DELETED:
            raise ListingArchivingError()
        if self.status == ListingStatus.ARCHIVED:
            return
        self.status = ListingStatus.ARCHIVED

    def delete(self):
        if self.status == ListingStatus.DELETED:
            return
        self.status = ListingStatus.DELETED

    def change_price(self, new_price: int, new_currency: PriceCurrency) -> None:
        self.price = new_price
        self.currency = new_currency

    def change_location(self, city_id: UUID) -> None:
        self.city_id = city_id

    def change_description(self, description: str) -> None:
        self.description = description
        
    def change_attributes(self, attributes: dict[str, Any]) -> None:
        self.attributes = attributes



