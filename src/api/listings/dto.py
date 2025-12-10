import enum
from typing import Optional, Dict, List, Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.references.dto import AllReferencesDTO
from src.core.listings.domain.enums import ListingCurrencyEnum, MimeTypeEnum, MachineryConditionEnum


class FieldTypeEnum(str, enum.Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    SELECT = "select"
    FILE = "file"


class FieldOptionDTO(BaseModel):
    value: str
    label: str


class FieldFormDTO(BaseModel):
    """Одно поле формы"""
    name: str
    label: str
    type: FieldTypeEnum
    required: bool = False
    placeholder: Optional[str] = None
    options_ref: Optional[str] = None
    options: Optional[List[FieldOptionDTO]] = None
    extra: Optional[Dict[str, Any]] = None


class FieldFormGroupDTO(BaseModel):
    """Группа полей"""
    id: str
    title: str
    order: int
    fields: List[FieldFormDTO]


class FormSchemaResponse(BaseModel):
    """Финальный ответ"""
    subcategory_id: UUID
    schema: List[FieldFormGroupDTO]
    references: AllReferencesDTO


class CreateListingDTO(BaseModel):
    roubric_id: UUID
    region_id: UUID
    title: str
    price: int
    currency: ListingCurrencyEnum
    description: Optional[str]
    media: list["CreateListingMediaDTO"]
    machinery: "CreateMachineryDTO"


class CreateListingMediaDTO(BaseModel):
    media_url: str
    mime_type: MimeTypeEnum
    file_size: int
    position: int


class CreateMachineryDTO(BaseModel):
    subcategory_id: UUID
    manufacturer_id: UUID
    manufacturer_country_id: UUID
    color_id: Optional[UUID] = None
    model: str
    year_of_issue: int
    condition: MachineryConditionEnum
    extra_specs: list["CreateExtraSpecsDTO"]


class CreateExtraSpecsDTO(BaseModel):
    key: str
    value: Any
    unit: str | None


class InitialListingMediaDTO(BaseModel):
    id: UUID
    media_url: str
    mime_type: MimeTypeEnum
    file_size: int
    position: int


class InitialExtraSpecsDTO(BaseModel):
    key: str
    value: Any
    unit: str | None


class InitialMachineryDTO(BaseModel):
    subcategory_id: UUID
    manufacturer_id: UUID
    manufacturer_country_id: UUID
    color_id: Optional[UUID] = None
    model: str
    year_of_issue: int
    condition: MachineryConditionEnum
    extra_specs: List[InitialExtraSpecsDTO]


class InitialListingDataDTO(BaseModel):
    roubric_id: UUID
    region_id: UUID
    title: str
    price: int
    currency: ListingCurrencyEnum
    description: Optional[str]
    media: List[InitialListingMediaDTO]
    machinery: "InitialMachineryDTO"


class UpdateListingFormSchemaDTO(BaseModel):
    listing_id: UUID
    form_schema: List[FieldFormGroupDTO]
    initial_listing_data: InitialListingDataDTO
    references: AllReferencesDTO


class UpdateListingMediaDTO(BaseModel):
    media_url: str
    mime_type: MimeTypeEnum
    file_size: int


class UpdateExtraSpecsDTO(BaseModel):
    key: str
    value: Any
    unit: str | None


class UpdateMachineryDTO(BaseModel):
    subcategory_id: UUID
    manufacturer_id: UUID
    manufacturer_country_id: UUID
    color_id: UUID
    model: str
    year_of_issue: int
    condition: MachineryConditionEnum
    extra_specs: List["UpdateExtraSpecsDTO"]


class UpdateListingDTO(BaseModel):
    roubric_id: UUID
    region_id: UUID
    title: str
    price: int
    currency: str
    description: str
    media: List[UpdateListingMediaDTO]
    machinery: UpdateMachineryDTO
