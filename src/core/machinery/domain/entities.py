from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from src.core.machinery.domain.enums import PriceCurrency, MachineryCondition, ListingStatus
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Machinery(AggregateRoot):
    id: UUID
    seller_id: UUID
    subcategory_id: UUID
    title: str | None
    price: int | None
    currency: PriceCurrency | None
    city_id: UUID | None
    description: str | None
    brand_id: UUID | None
    model: str | None
    year_of_issue: int | None
    condition: MachineryCondition | None
    color_id: UUID | None
    attributes: dict | None
    country_id: UUID | None
    status: ListingStatus
    created_at: datetime
    updated_at: datetime

    def activate(self):
        if self.status == ListingStatus.ACTIVE:
            return

        self.status = ListingStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)

    def update(self, validated_attributes: dict, **kwargs):
        self.attributes = validated_attributes

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self):
        if self.status == ListingStatus.INACTIVE:
            return

        self.status = ListingStatus.INACTIVE
        self.updated_at = datetime.now(timezone.utc)

    def delete(self):
        if self.status == ListingStatus.DELETED:
            return

        self.status = ListingStatus.DELETED
        self.updated_at = datetime.now(timezone.utc)
