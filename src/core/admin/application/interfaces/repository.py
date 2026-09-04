from abc import ABC, abstractmethod
from uuid import UUID

from src.core.admin.domain.entities import Admin


class IAdminRepository(ABC):
    @abstractmethod
    async def save(self, admin: Admin) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, admin_id: UUID) -> Admin:
        raise NotImplementedError

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID) -> Admin:
        raise NotImplementedError
