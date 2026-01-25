import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Wishlist(AggregateRoot):
    id: UUID
    buyer_id: UUID
    machinery_id: UUID

    @classmethod
    def create(cls, buyer_id: UUID, machinery_id: UUID):
        return cls(id=uuid.uuid4(), buyer_id=buyer_id, machinery_id=machinery_id)
