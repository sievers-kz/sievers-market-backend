from abc import ABC, abstractmethod
from uuid import UUID


class IWishlistCounter(ABC):
    @abstractmethod
    async def get_total_wishlist(self, machinery_id: UUID) -> int:
        raise NotImplementedError

