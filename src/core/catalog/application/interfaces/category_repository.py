from abc import ABC, abstractmethod
from uuid import UUID

from src.core.catalog.domain.entities import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, category: Category) -> None:
        raise NotImplementedError
