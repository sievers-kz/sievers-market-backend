from abc import ABC, abstractmethod
from uuid import UUID


class AbstractRegionService(ABC):
    @abstractmethod
    async def exists(self, region_id: UUID) -> bool:
        raise NotImplementedError
