from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from src.core.listings.domain.enums import ListingStatusEnum
from src.core.shared.domain.entities import AggregateRoot, Entity


@dataclass(frozen=False)
class Listing(AggregateRoot):
    id: UUID
    author_id: UUID
    roubric_id: UUID
    region_id: UUID | None
    title: str | None
    price: int | None
    currency: str | None
    description: str | None
    status: str
    media: List[ListingMedia] | None
    machinery: Machinery | None
    updated_at: datetime

    def can_be_published(self):
        if not self.title:
            raise ValueError("Заголовок обязателен")
        if not self.region_id:
            raise ValueError("Укажите местоположение")
        if not self.price or self.price == 0:
            raise ValueError("Цена должна быть указана")
        if not self.media:
            raise ValueError("Добавьте минимум одну фотографию")
        self.machinery.validate_required()

    def publish(self):
        if self.status == ListingStatusEnum.ACTIVE:
            raise ValueError("Объявление уже активировано")

        self.can_be_published()
        self.status = ListingStatusEnum.ACTIVE

    def deactivate(self):
        if self.status != ListingStatusEnum.ACTIVE:
            if self.status == ListingStatusEnum.INACTIVE:
                raise ValueError("Объявление уже деактивировано")
            raise ValueError("Деактивировать можно только активные объявления")
        self.status = ListingStatusEnum.INACTIVE

    def draft(self):
        self.status = ListingStatusEnum.DRAFT

    def archive(self):
        if self.status == ListingStatusEnum.ARCHIVED:
            raise ValueError("Объявление уже добавлено в архив")
        self.status = ListingStatusEnum.ARCHIVED

    def delete(self):
        if self.status == ListingStatusEnum.DELETED:
            raise ValueError("Объявление уже удалено")
        self.status = ListingStatusEnum.DELETED

    def update(self, raw_update_data: dict):
        self.region_id = raw_update_data["region_id"]
        self.title = raw_update_data["title"]
        self.price = raw_update_data["price"]
        self.currency = raw_update_data["currency"]
        self.description = raw_update_data["description"]
        self.update_media(raw_update_data["media"])
        self.machinery.update(raw_update_data["machinery"])

    def update_media(self, new_media_list: list[dict]):
        self.media.clear()
        new_collection = []

        for position, m_data in enumerate(new_media_list):
            new_media = ListingMedia(
                id=uuid.uuid4(),
                listing_id=self.id,
                media_url=m_data["media_url"],
                mime_type=m_data["mime_type"],
                file_size=m_data["file_size"],
                position=position,
                uploaded_at=datetime.utcnow()
            )

            new_collection.append(new_media)
        self.media = new_collection


@dataclass(frozen=False)
class ListingMedia(Entity):
    id: UUID
    listing_id: UUID
    media_url: str | None
    mime_type: str | None
    file_size: int | None
    position: int
    uploaded_at: datetime

    def update(self, raw_media: list[dict]):
        self.media_url = raw_media["media_url"]
        self.mime_type = raw_media["mime_type"]
        self.file_size = raw_media["file_size"]
        self.position = raw_media["position"]


@dataclass(frozen=False)
class Machinery(Entity):
    id: UUID
    listing_id: UUID
    subcategory_id: UUID
    manufacturer_id: UUID | None
    manufacturer_country_id: UUID | None
    color_id: UUID | None
    model: str | None
    year_of_issue: int | None
    condition: str | None
    extra_specs: dict | None

    def update(self, raw_machinery: dict):
        self.subcategory_id = raw_machinery["subcategory_id"]
        self.manufacturer_id = raw_machinery["manufacturer_id"]
        self.manufacturer_country_id = raw_machinery["manufacturer_country_id"]
        self.color_id = raw_machinery["color_id"]
        self.model = raw_machinery["model"]
        self.year_of_issue = raw_machinery["year_of_issue"]
        self.condition = raw_machinery["condition"]
        self.extra_specs = self.update_extra_specs(raw_machinery["extra_specs"])

    def update_extra_specs(self, raw_extra_specs: dict):
        result = []
        for spec in raw_extra_specs:
            item = {
                "key": spec["key"],
                "value": spec["value"],
                "unit": spec.get("unit"),
                "label": spec.get("label")
            }
            result.append(item)
        return result

    def validate_required(self):
        if not self.subcategory_id:
            raise ValueError("Подкатегория обязательна")
        if not self.manufacturer_id:
            raise ValueError("Нужно указать производителя")
        if not self.manufacturer_country_id:
            raise ValueError("Укажите страну-производителя")
        if not self.model:
            raise ValueError("Укажите модель")
        if not self.year_of_issue:
            raise ValueError("Укажите год выпуска")
        if not self.condition:
            raise ValueError("Укажите состояние техники")