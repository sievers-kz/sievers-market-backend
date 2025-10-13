from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel, Field, EmailStr, model_validator

from src.core.users.domain.enums import BusinessTypeEnum, UserRoleEnum


class UserDTO(BaseModel):
    role: UserRoleEnum
    first_name: str = Field(min_length=2, max_length=32, title="Имя")
    last_name: str = Field(min_length=2, max_length=32, title="Фамилия")
    patronymic: Optional[str] = Field(None, min_length=2, max_length=32, title="Отчество")
    email: str = Field(title="Email")
    phone: Optional[str] = Field(None, title="Номер телефона")
    profile: Union["IndividualUserDTO", "BusinessUserDTO"]
    authentication: "UserAuthDTO"

    @model_validator(mode="before")
    @classmethod
    def parse_profile(cls, data):
        role = data.get('role')
        profile_data = data.get('profile')

        if role == UserRoleEnum.BUSINESS or role == "business":
            data['profile'] = BusinessUserDTO(**profile_data)
        elif role == UserRoleEnum.INDIVIDUAL or role == "individual":
            data['profile'] = IndividualUserDTO(**profile_data)

        return data


class IndividualUserDTO(BaseModel):
    pass


class BusinessUserDTO(BaseModel):
    business_type: BusinessTypeEnum = Field(title="Тип юридического лица")
    organization_fullname: str = Field(title="Наименование организации")
    iin: str | None = Field(None, title="ИИН")
    bin: str | None = Field(None, title="БИН")


class UserAuthDTO(BaseModel):
    password: str = Field(title="Пароль")


class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str


class TokenDataDTO(BaseModel):
    token_str: str
    expires_at: datetime


class LoginResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class EmailConfirmationDTO(BaseModel):
    confirmation_code: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class ForgotPasswordDTO(BaseModel):
    email: EmailStr


class ResetPasswordDTO(BaseModel):
    reset_password_token: str
    new_password: str
