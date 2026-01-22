from abc import ABC, abstractmethod
from uuid import UUID

from typing_extensions import Any


class AbstractAttributeValidator(ABC):
    @abstractmethod
    async def validate(self, subcategory_id: UUID, raw_attributes: dict[str, Any],) -> dict[str, Any]:
        raise NotImplementedError


