from abc import ABC, abstractmethod
from uuid import UUID

from src.core.vendor.domain.entities import Vendor


class IVendorRepository(ABC):
    @abstractmethod
    async def save(self, vendor: Vendor) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_tax_id(self, tax_id: str) -> Vendor:
        raise NotImplementedError

    @abstractmethod
    async def get_by_account_id(self, account_id: UUID) -> Vendor:
        raise NotImplementedError
