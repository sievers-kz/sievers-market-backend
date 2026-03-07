from abc import ABC, abstractmethod
from uuid import UUID

from src.core.customer.domain.entities import Customer


class AbstractCustomerService(ABC):
    """Interface for open host service (OHS) using"""
    @abstractmethod
    async def create(self, account_id: UUID, last_name: str, first_name: str) -> Customer:
        raise NotImplementedError
