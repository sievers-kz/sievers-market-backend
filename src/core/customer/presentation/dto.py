from uuid import UUID

from pydantic import BaseModel

from src.core.shared.presentation.dto import DTO


class ChangeCustomerFullname(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None


class CreateCustomerRequest(DTO):
    last_name: str
    first_name: str


class CustomerProfileResponse(DTO):
    customer_id: UUID
    last_name: str
    first_name: str
    patronymic: str | None
    email: str
    avatar_url: str | None
