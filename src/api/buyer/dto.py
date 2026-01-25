from uuid import UUID

from pydantic import BaseModel


class ChangeFullname(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None


class ChangeBuyerRegion(BaseModel):
    region_id: UUID


class BuyerResponse(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None
    avatar_url: str | None = None

