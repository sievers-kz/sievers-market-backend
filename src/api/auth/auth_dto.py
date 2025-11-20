from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.api.users.user_dto import BusinessDetailsDTO, UserProfileDTO, UserDTO
from src.core.auth.domain.enums import TokenTypeEnum


class CreateUserDTO(BaseModel):
    user: UserDTO
    profile: UserProfileDTO
    credentials: "UserCredentialsDTO"
    business_details: Optional[BusinessDetailsDTO] = None


class UserIdentityDTO(BaseModel):
    credentials: "UserCredentialsDTO"
    tokens: "AuthTokenDTO"


class UserCredentialsDTO(BaseModel):
    raw_password: str
    # password_changed_at: datetime


class AuthTokenDTO(BaseModel):
    token_type: TokenTypeEnum
    token_value: str
    is_revoked: bool
    expires_at: datetime


class LoginUserDTO(BaseModel):
    email: EmailStr
    raw_password: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class ForgotPasswordDTO(BaseModel):
    email: EmailStr


class LoginResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class EmailConfirmationDTO(BaseModel):
    confirmation_code: str


class ResetPasswordDTO(BaseModel):
    reset_password_token: str
    new_password: str


