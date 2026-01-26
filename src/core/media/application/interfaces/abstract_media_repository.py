from abc import ABC, abstractmethod
from uuid import UUID


class AbstractMediaRepository(ABC):
    @abstractmethod
    async def save(self, media):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_ids(self, media_ids: list[UUID]):
        raise NotImplementedError

    @abstractmethod
    async def get_max_position(self, machinery_id: UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_media_by_machinery_id(self, machinery_id: UUID):
        raise NotImplementedError
