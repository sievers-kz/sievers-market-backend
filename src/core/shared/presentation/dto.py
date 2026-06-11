from typing import TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.core.iam.domain.enums import UserRole


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CurrentUser(DTO):
    id: UUID


class CurrentCustomer(DTO):
    id: UUID


class CurrentVendor(DTO):
    id: UUID


T = TypeVar("T")


class PaginatedResponse(DTO, Generic[T]):
    items: list[T]
    total: int
    page: int
    pages: int
