from abc import ABC, abstractmethod
from uuid import UUID

from src.core.buyer.domain.entities import Buyer


class AbstractBuyerService(ABC):
    """Interface for open host service (OHS) using"""
    @abstractmethod
    async def create(self, account_id: UUID, buyer_data) -> Buyer:
        raise NotImplementedError
