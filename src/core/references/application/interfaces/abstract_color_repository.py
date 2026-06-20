from abc import ABC, abstractmethod
from uuid import UUID

from src.core.references.domain.entities import Color


class IColorRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Color]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, color_id: UUID) -> Color:
        raise NotImplementedError

    @abstractmethod
    async def save(self, color: Color) -> None:
        raise NotImplementedError
