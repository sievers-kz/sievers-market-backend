import enum
from datetime import datetime
from typing import Optional, Dict, List, Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.references.dto import AllReferencesDTO, SubcategoryResponse, RegionDTO, ManufacturerDTO, \
    ManufactureCountryDTO, ColorDTO
from src.core.listings.domain.enums import ListingCurrencyEnum, MimeTypeEnum, MachineryConditionEnum, ListingStatusEnum


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
    form_schema: List[FieldFormGroupDTO]
    references: AllReferencesDTO


class CreateActiveListingDTO(BaseModel):
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
    label: str


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
    label: str


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
    label: str


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


class UserListingsQueryDTO(BaseModel):
    id: UUID
    title: str | None
    price: int | None
    media: str | None
    status: ListingStatusEnum
    condition: MachineryConditionEnum | None
    subcategory: str
    updated_at: datetime


class CreateDraftListingDTO(BaseModel):
    roubric_id: UUID
    region_id: UUID | None
    title: str | None
    price: int | None
    currency: ListingCurrencyEnum | None
    description: Optional[str] | None
    media: list["CreateDraftListingMediaDTO"] | None
    machinery: Optional["CreateDraftMachineryDTO"]


class CreateDraftListingMediaDTO(BaseModel):
    media_url: str | None
    mime_type: MimeTypeEnum | None
    file_size: int | None


class CreateDraftMachineryDTO(BaseModel):
    subcategory_id: UUID | None
    manufacturer_id: UUID | None
    manufacturer_country_id: UUID | None
    color_id: Optional[UUID] = None
    model: str | None
    year_of_issue: int | None
    condition: MachineryConditionEnum | None
    extra_specs: list["CreateDraftExtraSpecsDTO"] | None


class CreateDraftExtraSpecsDTO(BaseModel):
    key: str | None
    value: Any | None
    unit: str | None
    label: str | None


class BaseFilters(BaseModel):
    subcategories: list[dict]
    price_range: dict


class DynamicFilters(BaseModel):
    key: str
    label: str
    type: str
    unit: Optional[dict] = None
    options: List["FilterOptions"] | None = None


class FilterTypes(str, enum.Enum):
    RANGE = "range"
    SELECT = "select"


class FilterOptions(BaseModel):
    value: str
    label: str


class FilterRanges(BaseModel):
    min_label: str
    max_label: str


class FilterFields(BaseModel):
    name: str
    label: str
    type: FilterTypes
    unit: Optional[dict] = None
    placeholder: str | None = None
    options: List[FilterOptions] | None = None
    ranges: FilterRanges | None = None


class FilterBlocks(BaseModel):
    id: str
    title: str
    order: int
    filters: List[FilterFields]


class SidebarFilters(BaseModel):
    base_filters: List[FilterBlocks]
    dynamic_filters: List[FilterBlocks] | None


class ListingCards(BaseModel):
    id: UUID
    title: str | None
    price: int | None
    media: str | None
    status: ListingStatusEnum
    condition: MachineryConditionEnum | None
    subcategory: str
    updated_at: datetime


class PaginationInfo(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class PublicListingsPageResponse(BaseModel):
    filters: SidebarFilters
    listings: List[ListingCards]
    pagination: PaginationInfo


class ListingAuthorDTO(BaseModel):
    id: UUID
    role: str
    email: str
    phone: str


class ListingMediaDTO(BaseModel):
    id: UUID
    media_url: str


class ListingMachineryDTO(BaseModel):
    id: UUID
    model: str
    year_of_issue: int
    condition: MachineryConditionEnum
    extra_specs: List[InitialExtraSpecsDTO]
    subcategory: SubcategoryResponse
    manufacturer: ManufacturerDTO
    manufacturer_country: ManufactureCountryDTO
    color: Optional[ColorDTO] = None


class DetailListingResponse(BaseModel):
    id: UUID
    title: str
    price: int
    currency: ListingCurrencyEnum
    description: str
    status: ListingStatusEnum
    author: ListingAuthorDTO
    region: RegionDTO
    media: List[ListingMediaDTO]
    machinery: ListingMachineryDTO
