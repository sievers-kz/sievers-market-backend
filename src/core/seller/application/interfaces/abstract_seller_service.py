from abc import ABC, abstractmethod
from uuid import UUID

from src.core.seller.domain.entities import Seller


class AbstractSellerService(ABC):
    @abstractmethod
    async def create(self, account_id: UUID, seller_data) -> Seller:
        raise NotImplementedError
