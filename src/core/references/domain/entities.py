import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.shared.domain.entities import Entity


@dataclass(frozen=False)
class Brand(Entity):
    id: UUID
    name: str

    @classmethod
    def create(cls, name: str):
        return cls(id=uuid.uuid4(), name=name)

    def update(self, name: str):
        self.name = name


@dataclass(frozen=False)
class Color(Entity):
    id: UUID
    name: str
    hex: str

    @classmethod
    def create(cls, name: str, hex: str):
        return cls(id=uuid.uuid4(), name=name, hex=hex)

    def update(self, name: str, hex: str):
        self.name = name
        self.hex = hex
