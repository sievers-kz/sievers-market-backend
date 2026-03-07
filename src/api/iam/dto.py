from datetime import datetime
from typing import Optional, Literal, Union, Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.core.iam.domain.enums import TokenType


class ResendCodeRequest(BaseModel):
    email: EmailStr


class ChangePasswordData(BaseModel):
    raw_password: str
    new_password: str


class TokenData(BaseModel):
    type: TokenType
    value: str
    expires_at: datetime


class ForgotPasswordData(BaseModel):
    email: EmailStr


class ResetPasswordData(BaseModel):
    raw_password: str
    password_reset_token: str


class RefreshData(BaseModel):
    refresh_token: str


class LoginAccount(BaseModel):
    email: EmailStr
    raw_password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class AccountConfirmation(BaseModel):
    confirm_token: str


class CreateUserRequest(BaseModel):
    email: EmailStr
    raw_password: str
    last_name: str
    first_name: str




