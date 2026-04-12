import uuid
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.core.machinery.domain.enums import MachineryCondition
from src.core.machinery.domain.value_objects import Title, Price, YearOfIssue, Description
from src.core.shared.domain.entities import AggregateRoot
from src.core.shared.domain.enums import PriceCurrency, ListingStatus


@dataclass(frozen=False)
class Machinery(AggregateRoot):
    id: UUID
    customer_id: UUID
    subcategory_id: UUID
    title: Title
    price: Price
    currency: PriceCurrency
    city_id: UUID
    description: Description | None
    brand_id: UUID
    model: str | None
    year_of_issue: YearOfIssue
    condition: MachineryCondition
    color_id: UUID | None
    country_id: UUID | None
    attributes: dict
    status: ListingStatus

    def activate(self):
        if self.status == ListingStatus.ACTIVE:
            raise ValueError("Объявление уже активировано")
        self.status = ListingStatus.ACTIVE

    def deactivate(self):
        if self.status == ListingStatus.INACTIVE:
            raise ValueError("Объявление уже деактивировано")
        self.status = ListingStatus.INACTIVE

    def archive(self):
        if self.status == ListingStatus.ARCHIVED:
            raise ValueError("Объявление уже архивировано")
        self.status = ListingStatus.ARCHIVED

    def delete(self):
        """Soft delete the entity"""
        if self.status == ListingStatus.DELETED:
            raise ValueError("Объявление уже удалено")
        self.status = ListingStatus.DELETED

    def change_general(self, brand_id: UUID, model: str, color_id: UUID, country_id: UUID):
        self.brand_id = brand_id
        self.model = model
        self.color_id = color_id
        self.country_id = country_id

    def change_operating_history(self, year_of_issue: int, condition: MachineryCondition):
        self.year_of_issue = YearOfIssue(value=year_of_issue)
        self.condition = MachineryCondition(condition)

    def change_price(self, raw_price: int, raw_currency: str):
        self.price = Price(value=raw_price)
        self.currency = PriceCurrency(raw_currency)

    def change_spec(self, spec: dict[str, Any]):
        self.attributes = spec

    def change_description(self, description: str):
        self.description = Description(value=description)
