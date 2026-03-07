from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.core.iam.domain.enums import UserRole


class CurrentUser(BaseModel):
    id: UUID


class CurrentCustomer(BaseModel):
    id: UUID


class CurrentSeller(BaseModel):
    id: UUID


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
