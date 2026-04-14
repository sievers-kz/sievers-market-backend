from uuid import UUID

from pydantic import BaseModel


class ChangeCustomerFullname(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None


class CustomerResponse(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None
    avatar_url: str | None = None

