from abc import ABC, abstractmethod
from uuid import UUID

from src.core.customer.domain.entities import Customer


class AbstractCustomerRepository(ABC):
    @abstractmethod
    async def save(self, customer: Customer) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID) -> Customer:
        raise NotImplementedError
