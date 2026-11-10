from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import (
    ListingAccessDeniedError,
    ListingDeletedError,
)
from src.core.listing.domain.value_objects import Gallery
from src.core.shared.domain.entities import AggregateRoot
from src.core.shared.domain.enums import PriceCurrency


@dataclass(frozen=False)
class Listing(AggregateRoot):
    id: UUID
    organization_id: UUID
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
    # TODO: добавить поле deleted_at и реализовать метод restore() с _days_since_deletion()

    def ensure_owned_by(self, organization_id: UUID) -> None:
        if self.organization_id != organization_id:
            raise ListingAccessDeniedError()

    def activate(self, organization_id: UUID) -> None:
        self.ensure_owned_by(organization_id)

        if self.status == ListingStatus.DELETED:
            raise ListingDeletedError()
        if self.status == ListingStatus.ACTIVE:
            return
        self.status = ListingStatus.ACTIVE

    def deactivate(self, organization_id: UUID) -> None:
        self.ensure_owned_by(organization_id)

        if self.status == ListingStatus.DELETED:
            raise ListingDeletedError()
        if self.status == ListingStatus.INACTIVE:
            return
        self.status = ListingStatus.INACTIVE

    def archive(self, organization_id: UUID) -> None:
        self.ensure_owned_by(organization_id)

        if self.status == ListingStatus.DELETED:
            raise ListingDeletedError()
        if self.status == ListingStatus.ARCHIVED:
            return
        self.status = ListingStatus.ARCHIVED

    def delete(self, organization_id: UUID) -> None:
        self.ensure_owned_by(organization_id)

        if self.status == ListingStatus.DELETED:
            return
        self.status = ListingStatus.DELETED

    def change_price(self, organization_id: UUID, new_price: int, new_currency: PriceCurrency) -> None:
        self.ensure_owned_by(organization_id)
        self.price = new_price
        self.currency = new_currency

    def change_location(self, organization_id: UUID, city_id: UUID) -> None:
        self.ensure_owned_by(organization_id)
        self.city_id = city_id

    def change_description(self, organization_id: UUID, description: str) -> None:
        self.ensure_owned_by(organization_id)
        self.description = description

    def change_attributes(self, organization_id: UUID, attributes: dict[str, Any]) -> None:
        self.ensure_owned_by(organization_id)
        self.attributes = attributes
