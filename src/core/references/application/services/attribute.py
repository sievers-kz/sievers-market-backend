from typing import Any
from uuid import UUID

from pydantic import ConfigDict, create_model, ValidationError

from src.core.references.application.interfaces.abstract_attribute_repository import AbstractAttributeRepository


_TYPE_MAP: dict[str, type] = {
    "integer": int,
    "float": float,
    "boolean": bool,
    "string": str,
}


class AttributeService:
    def __init__(self, repository: AbstractAttributeRepository):
        self.repository = repository

    async def validate(self, subcategory_id: UUID, raw_attributes: dict[str, Any]) -> dict[str, Any]:
        raw_attributes = raw_attributes or {}

        rules = await self.repository.get_by_subcategory_id(subcategory_id)
        if not rules:
            raise ValueError("Subcategory not found")

        fields = {
            rule.attribute.key: (
                _TYPE_MAP.get(rule.attribute.value_type.value, str),
                ... if rule.is_required else None,
            )
            for rule in rules
        }

        model = create_model(
            "DynamicAttributes",
            __config__=ConfigDict(extra="forbid"),
            **fields,
        )

        try:
            return model(**raw_attributes).model_dump(exclude_unset=True)
        except ValidationError as e:
            raise ValueError(e.errors())
