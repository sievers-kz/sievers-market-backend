from abc import ABC, abstractmethod

from src.core.references.domain.entities import Brand


class IBrandRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Brand]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, brand_id: int) -> Brand:
        raise NotImplementedError

    @abstractmethod
    async def save(self, brand: Brand) -> None:
        raise NotImplementedError
