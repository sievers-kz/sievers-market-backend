from abc import ABC, abstractmethod
from uuid import UUID

from src.core.buyer.domain.entities import Buyer


class AbstractBuyerRepository(ABC):
    @abstractmethod
    async def save(self, buyer: Buyer) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID) -> Buyer:
        raise NotImplementedError
