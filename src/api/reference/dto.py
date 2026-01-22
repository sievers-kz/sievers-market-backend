from typing import Optional, List, Any, Literal, Annotated, Union
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.machinery.domain.enums import MachineryCondition


class BrandDTO(BaseModel):
    id: UUID
    name: str


class RegionDTO(BaseModel):
    id: UUID
    name: str


class CountryDTO(BaseModel):
    id: UUID
    name: str


class ColorDTO(BaseModel):
    id: UUID
    name: str
    hex: str


class Option(BaseModel):
    key: str
    label: str


class FilterAttribute(BaseModel):
    key: str
    label: str
    unit: str | None = None
    widget_type: str
    required: bool
    options: list[Option] | None = None


class FormField(BaseModel):
    key: str
    label: str
    widget_type: Literal["text", "number", "select", "range"]
    required: bool = False
    data_url: str | None = None
    options: list[Option] | None = None
    unit: str | None = None


class MachineryConfig(BaseModel):
    rubric: Literal["machinery"] = "machinery"
    fields: list[dict] = [
        {
            "key": "brand_id",
            "label": "Марка",
            "widget_type": "select",
            "required": True,
            "data_url": "/api/v1/reference/brands"
        },

        {
            "key": "country_id",
            "label": "Страна",
            "widget_type": "select",
            "required": False,
            "data_url": "/api/v1/reference/countries"
        },

        {
            "key": "color_id",
            "label": "Цвет",
            "widget_type": "select",
            "required": False,
            "data_url": "/api/v1/reference/colors"
        },

        {
            "key": "model",
            "label": "Модель",
            "widget_type": "text",
            "required": False,
        },

        {
            "key": "year_of_issue",
            "label": "Год выпуска",
            "widget_type": "number",
            "required": True,
            "min_value": 1900,
            "max_value": 2026
        },

        {
            "key": "condition",
            "label": "Состояние",
            "widget_type": "select",
            "required": True,
            "options": [
                {"key": item.value, "label": item.label}
                for item in MachineryCondition
            ]
        }
    ]


class LivestockConfig(BaseModel):
    rubric: Literal["livestock"] = "livestock"
    fields: list[dict] = []


FormConfig = Annotated[Union[MachineryConfig, LivestockConfig], Field(discriminator="rubric")]