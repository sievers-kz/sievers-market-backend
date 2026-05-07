from abc import abstractmethod, ABC
from uuid import UUID

from src.core.catalog.domain.entities import Subcategory


class ISubcategoryRepository(ABC):
    @abstractmethod
    async def get_by_id(self, subcategory_id: UUID) -> Subcategory:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Subcategory]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, subcategory: Subcategory) -> None:
        raise NotImplementedError
