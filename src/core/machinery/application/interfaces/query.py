from abc import ABC, abstractmethod
from uuid import UUID

from src.core.shared.domain.enums import ListingStatus


class IMachineryQuery(ABC):
    @abstractmethod
    async def get_machinery_list(self, filters, page: int, limit: int):
        raise NotImplementedError

    @abstractmethod
    async def get_machinery_detail(self, machinery_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_customer_machinery(self, customer_id: UUID, filters, page: int, limit: int):
        raise NotImplementedError
