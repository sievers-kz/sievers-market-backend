from typing import Any
from uuid import UUID

from src.core.machinery.application.interfaces.abstract_attribute_validator import AbstractAttributeValidator
from src.core.references.application.services.attribute import AttributeService


class AttributeValidator(AbstractAttributeValidator):
    def __init__(self, attribute_service: AttributeService):
        self.attribute_service = attribute_service

    async def validate(self, subcategory_id: UUID, raw_attributes: dict[str, Any]) -> dict[str, Any]:
        return await self.attribute_service.validate(subcategory_id, raw_attributes)
