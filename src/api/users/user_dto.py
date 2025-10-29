from typing import Optional

from pydantic import BaseModel

from src.api.auth.auth_dto import UserCredentialsDTO
from src.core.users.domain.enums import BusinessTypeEnum, UserRoleEnum, DocumentTypeEnum


class CreateUserDTO(BaseModel):
    role: UserRoleEnum
    email: str
    phone: str
    profile: "UserProfileDTO"
    credentials: "UserCredentialsDTO"
    business_details: Optional["BusinessDetailsDTO"] = None


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


class EmailConfirmationDTO(BaseModel):
    confirmation_code: str


class ResetPasswordDTO(BaseModel):
    reset_password_token: str
    new_password: str
