from typing import Optional, List, Any
from uuid import UUID

from pydantic import BaseModel, Field


class SubcategoryResponse(BaseModel):
    id: UUID
    category_id: UUID
    name: str


class CategoryResponse(BaseModel):
    id: UUID
    roubric_id: UUID
    name: str
    subcategories: Optional[List[SubcategoryResponse]] = Field(default_factory=list)


class RoubricResponse(BaseModel):
    id: UUID
    name: str
    categories: Optional[List[CategoryResponse]] = Field(default_factory=list)


class ManufacturerDTO(BaseModel):
    id: UUID
    name: str


class ManufactureCountryDTO(BaseModel):
    id: UUID
    name: str


class RegionDTO(BaseModel):
    id: UUID
    name: str


class ColorDTO(BaseModel):
    id: UUID
    name: str
    hex: str


class SpecificationDTO(BaseModel):
    id: UUID
    key: str
    label: str
    value_type: str
    unit: str | None = None
    position: int
    is_required: bool
    options: Any | None = None


class AllReferencesDTO(BaseModel):
    manufacturers: List[ManufacturerDTO]
    manufacture_countries: List[ManufactureCountryDTO]
    regions: List[RegionDTO]
    colors: List[ColorDTO]
