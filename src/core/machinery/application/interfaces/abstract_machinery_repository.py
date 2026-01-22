from abc import ABC, abstractmethod
from uuid import UUID

from src.core.machinery.domain.entities import Machinery


class AbstractMachineryRepository(ABC):
    @abstractmethod
    async def save(self, machinery: Machinery) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_machinery_id(self, machinery_id: UUID) -> Machinery:
        raise NotImplementedError
