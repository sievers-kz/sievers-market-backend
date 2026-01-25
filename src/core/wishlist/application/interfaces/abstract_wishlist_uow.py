from abc import abstractmethod, ABC

from src.core.wishlist.application.interfaces.abstract_wishlist_repository import AbstractWishlistRepository


class AbstractWishlistUnitOfWork(ABC):
    @property
    @abstractmethod
    def wishlist(self) -> AbstractWishlistRepository:
        raise NotImplementedError
