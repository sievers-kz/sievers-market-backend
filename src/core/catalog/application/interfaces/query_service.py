from abc import ABC, abstractmethod
from uuid import UUID

from src.core.catalog.presentation.dto.catalog import AttributeResponse, RubricResponse


class ICatalogQueryService(ABC):
    @abstractmethod
    async def get_subcategory_attributes(
        self, subcategory_id: UUID
    ) -> list[AttributeResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_category_tree(self) -> list[RubricResponse]:
        raise NotImplementedError
