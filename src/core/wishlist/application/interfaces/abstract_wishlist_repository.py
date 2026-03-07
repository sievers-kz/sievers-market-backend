from abc import ABC, abstractmethod
from uuid import UUID

from src.core.wishlist.domain.entities import Wishlist


class AbstractWishlistRepository(ABC):
    @abstractmethod
    async def save(self, wishlist: Wishlist) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count_total_wishlist(self, machinery_id: UUID) -> int:
        raise NotImplementedError
