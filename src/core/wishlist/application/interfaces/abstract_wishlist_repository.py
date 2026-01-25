from abc import ABC, abstractmethod

from src.core.wishlist.domain.entities import Wishlist


class AbstractWishlistRepository(ABC):
    @abstractmethod
    async def save(self, wishlist: Wishlist) -> None:
        raise NotImplementedError
