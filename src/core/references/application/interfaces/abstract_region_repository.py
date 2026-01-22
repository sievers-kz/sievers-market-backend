from abc import abstractmethod, ABC
from uuid import UUID


class AbstractRegionRepository(ABC):
    @abstractmethod
    async def exists(self, region_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
