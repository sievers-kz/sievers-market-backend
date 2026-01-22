from typing import Any
from uuid import UUID

from src.core.references.application.interfaces.abstract_attribute_repository import AbstractAttributeRepository


class AttributeService:
    def __init__(self, repository: AbstractAttributeRepository):
        self.repository = repository

    async def validate(self, subcategory_id: UUID, raw_attributes: dict[str, Any]) -> dict[str, Any]:
        raw_attributes = raw_attributes or {}

        rules = await self.repository.get_by_subcategory_id(subcategory_id)
        if not rules:
            raise ValueError("Subcategory not found")

        map_rules = {rule.attribute.key: rule for rule in rules}

        allowed_keys = set(map_rules.keys())
        received_keys = set(raw_attributes.keys())

        unknown_keys = received_keys - allowed_keys
        if unknown_keys:
            raise ValueError(f"Unknown attributes: {', '.join(unknown_keys)}")

        clean_attributes = {}

        for key, rule in map_rules.items():
            value = raw_attributes.get(key)

            if value in [None, ""]:
                raise ValueError(f"Missing required attribute {key}")

            try:
                target_type = rule.attribute.value_type
                casted_value = self._cast_value(key, value, target_type)
                clean_attributes[key] = casted_value
            except ValueError:
                raise ValueError(f"Invalid value for attribute {key}")
        return clean_attributes

    def _cast_value(self, key: str, value: Any, target_type: str) -> Any:
        try:
            if target_type == "integer":
                return int(value)
            elif target_type == "float":
                if isinstance(value, str):
                    value = value.replace(",", ".")
                return float(value)
            elif target_type == "boolean":
                return bool(value)
            return str(value)
        except Exception:
            raise ValueError(f"Invalid value for attribute {key}")

