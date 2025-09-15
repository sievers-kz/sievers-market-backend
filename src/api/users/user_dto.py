from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel, Field, EmailStr, model_validator

from src.core.users.domain.enums import BusinessTypeEnum, UserRoleEnum


class UserDTO(BaseModel):
    role: UserRoleEnum
    first_name: str = Field(min_length=2, max_length=32)
    last_name: str = Field(min_length=2, max_length=32)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=32)
    email: EmailStr
    phone: Optional[str] = Field(None)
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
    business_type: BusinessTypeEnum
    organization_fullname: str
    iin: str | None = None
    bin: str | None = None


class UserAuthDTO(BaseModel):
    password: str


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
