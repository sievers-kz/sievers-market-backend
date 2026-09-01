from abc import ABC, abstractmethod
from uuid import UUID

from src.core.media.domain.entities import Media


class IMediaRepository(ABC):
    @abstractmethod
    async def save(self, media: Media) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, media_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, media_id: UUID) -> Media:
        raise NotImplementedError
