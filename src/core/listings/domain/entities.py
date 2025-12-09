from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.shared.domain.entities import AggregateRoot, Entity


@dataclass(frozen=False)
class Listing(AggregateRoot):
    id: UUID
    author_id: UUID
    roubric_id: UUID
    region_id: UUID
    title: str
    price: int
    currency: str
    description: str
    status: str
    media: list["ListingMedia"]
    machinery: "Machinery"


@dataclass(frozen=False)
class ListingMedia(Entity):
    id: UUID
    listing_id: UUID
    media_url: str
    mime_type: str
    is_main: bool
    file_size: int
    position: int
    uploaded_at: datetime


@dataclass(frozen=False)
class Machinery(Entity):
    id: UUID
    listing_id: UUID
    subcategory_id: UUID
    manufacturer_id: UUID
    manufacturer_country_id: UUID
    color_id: UUID
    model: str
    year_of_issue: int
    condition: str
    extra_specs: dict


