from abc import ABC, abstractmethod
from uuid import UUID

from src.core.catalog.domain.entities import Rubric


class IRubricRepository(ABC):
    @abstractmethod
    async def get_by_id(self, rubric_id: UUID) -> Rubric:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Rubric]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, rubric: Rubric) -> None:
        raise NotImplementedError
