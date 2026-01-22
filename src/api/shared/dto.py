from uuid import UUID

from pydantic import BaseModel

from src.core.iam.domain.enums import UserRole


class CurrentUser(BaseModel):
    id: UUID
    role: UserRole


class CurrentSeller(BaseModel):
    id: UUID
