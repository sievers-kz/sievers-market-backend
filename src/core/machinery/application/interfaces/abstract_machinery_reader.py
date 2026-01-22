from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.core.machinery.domain.enums import ListingStatus


class AbstractMachineryReader(ABC):
    @abstractmethod
    async def get_seller_machinery(
        self,
        seller_id: UUID,
        status: ListingStatus,
        page: int,
        limit: int
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_detail_machinery(self, machinery_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_owner_detail_machinery(self, machinery_id: UUID, seller_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        category_id: UUID | None,
        subcategory_id: UUID | None,
        min_price: int | None,
        max_price: int | None,
        city_id: UUID | None,
        dynamic_filters: dict[str, Any] | None,
        page: int = 1,
        limit: int = 20
    ):
        raise NotImplementedError
