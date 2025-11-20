from typing import Optional

from pydantic import BaseModel

from src.core.users.domain.enums import BusinessTypeEnum, DocumentTypeEnum, UserRoleEnum


class UserDTO(BaseModel):
    role: UserRoleEnum
    email: str
    phone: str


class UserProfileDTO(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None
    avatar_url: str | None = None


class BusinessDetailsDTO(BaseModel):
    business_type: BusinessTypeEnum
    organization_fullname: str
    document_type: DocumentTypeEnum
    document_value: str


class FullnameDTO(BaseModel):
    access_token: str
    last_name: str
    first_name: str
    patronymic: Optional[str] = None


class EmailDTO(BaseModel):
    access_token: str
    email: str


class PhoneDTO(BaseModel):
    access_token: str
    phone: str


class OrganizationFullnameDTO(BaseModel):
    access_token: str
    organization_fullname: str


class DocumentValueDTO(BaseModel):
    access_token: str
    document_value: str


class AvatarUrlDTO(BaseModel):
    access_token: str
    avatar_url: str


class ChangePasswordDTO(BaseModel):
    access_token: str
    old_password: str
    new_password: str
