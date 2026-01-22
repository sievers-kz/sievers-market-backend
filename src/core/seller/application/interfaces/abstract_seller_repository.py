from abc import ABC, abstractmethod
from uuid import UUID

from src.core.seller.domain.entities import Seller


class AbstractSellerRepository(ABC):
    @abstractmethod
    async def save(self, seller: Seller) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID) -> Seller:
        raise NotImplementedError
