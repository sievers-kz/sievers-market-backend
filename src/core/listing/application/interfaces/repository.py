from abc import ABC, abstractmethod
from uuid import UUID

from src.core.listing.domain.entities import Listing


class IListingRepository(ABC):
    @abstractmethod
    async def save(self, listing: Listing) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, listing_id: UUID) -> Listing:
        raise NotImplementedError
