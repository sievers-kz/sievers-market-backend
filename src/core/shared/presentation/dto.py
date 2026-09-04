from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CurrentUser(DTO):
    id: UUID


class CurrentCustomer(DTO):
    id: UUID


class CurrentVendor(DTO):
    id: UUID


class CurrentAdmin(DTO):
    id: UUID


T = TypeVar("T")


class PaginatedResponse(DTO, Generic[T]):
    items: list[T]
    total: int
    page: int
    pages: int


class SearchResult(DTO):
    hits: list[dict]
    total: int
    page: int
    pages: int


class SearchIndexConfig(DTO):
    filterable: list[str] = []
    sortable: list[str] = []
    searchable: list[str] = []
