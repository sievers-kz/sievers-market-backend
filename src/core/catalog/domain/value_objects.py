from dataclasses import dataclass
from typing import Any

from src.core.catalog.domain.enums import AttributeType
from src.core.catalog.domain.exceptions import (
    AttributeOptionError,
    AttributeRequiredError,
    AttributeTypeError,
)


@dataclass(frozen=True)
class Attribute:
    key: str
    label: str
    type: AttributeType
    required: bool = False
    filterable: bool = False
    unit: str | None = None
    options: list[str] | None = None
    source: str | None = None
    position: int = 0

    def __post_init__(self):
        pass

    def validate_value(self, value: Any) -> Any:
        self._validate_key_required(value)
        if value is None:
            return None
        return self._cast_type(value)

    def _validate_key_required(self, value: Any) -> None:
        if self.required and (value is None or value == ""):
            raise AttributeRequiredError(field=self.label)

    def _cast_type(self, value: Any) -> Any:
        try:
            if self.type == AttributeType.INTEGER:
                return int(value)
            if self.type == AttributeType.FLOAT:
                return float(value)
            if self.type == AttributeType.BOOLEAN:
                return str(value).lower() in ("true", "1", "yes")
            if self.type == AttributeType.ENUMERATE:
                if value not in (self.options or []):
                    raise AttributeOptionError()
                return value
            return str(value)
        except (ValueError, TypeError):
            raise AttributeTypeError(field=self.label)

    @classmethod
    def from_dict(cls, data: dict) -> "Attribute":
        return cls(
            key=data["key"],
            label=data["label"],
            type=AttributeType(data["type"]),
            required=data.get("required", False),
            filterable=data.get("filterable", False),
            unit=data.get("unit"),
            options=data.get("options"),
            position=data["position"],
        )

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "label": self.label,
            "type": self.type,
            "required": self.required,
            "filterable": self.filterable,
            "unit": self.unit,
            "options": self.options,
            "position": self.position,
        }
