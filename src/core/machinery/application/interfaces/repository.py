from abc import ABC, abstractmethod
from uuid import UUID

from src.core.machinery.domain.entities import Machinery


class IMachineryRepository(ABC):
    @abstractmethod
    async def save(self, machinery: Machinery) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_machinery_by_id(self, machinery_id: UUID) -> Machinery:
        raise NotImplementedError

    @abstractmethod
    async def count_customer_machinery(self, customer_id: UUID) -> list[Machinery]:
        raise NotImplementedError
