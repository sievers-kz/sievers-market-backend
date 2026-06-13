from abc import ABC, abstractmethod
from uuid import UUID

from src.core.iam.domain.entities import Account


class IAccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account):
        raise NotImplementedError

    @abstractmethod
    async def get_account_by_id(self, account_id: UUID) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def find_by_token_value(self, token_value: str) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def get_account_by_email(self, email: str) -> Account:
        raise NotImplementedError
