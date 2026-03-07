from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IAttributeValidator(ABC):
    @abstractmethod
    async def validate(self, subcategory_id: UUID, attributes: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
