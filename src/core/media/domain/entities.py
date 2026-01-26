from dataclasses import dataclass
from uuid import UUID

from src.core.media.domain.enums import MediaType
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Media(AggregateRoot):
    id: UUID
    machinery_id: UUID
    media_url: str
    media_type: MediaType
    media_size: int
    position: int
