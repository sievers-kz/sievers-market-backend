import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.media.domain.enums import MediaType
from src.core.media.domain.value_objects import MediaSize
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Media(AggregateRoot):
    id: UUID
    owner_id: UUID
    media_url: str
    media_type: MediaType
    media_size: MediaSize

    @classmethod
    def create(
        cls,
        owner_id: UUID,
        media_url: str,
        media_type: MediaType,
        media_size: MediaSize,
    ) -> "Media":
        return cls(
            id=uuid.uuid4(),
            owner_id=owner_id,
            media_url=media_url,
            media_type=media_type,
            media_size=media_size,
        )
