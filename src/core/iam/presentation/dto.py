from datetime import datetime
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.core.customer.presentation.dto import CustomerProfileResponse
from src.core.iam.domain.enums import TokenType
from src.core.shared.presentation.dto import DTO
from src.core.vendor.presentation.dto import VendorProfileResponse


class CustomerMeResponse(DTO):
    role: Literal["customer"] = "customer"
    profile: CustomerProfileResponse


class VendorMeResponse(DTO):
    role: Literal["vendor"] = "vendor"
    profile: VendorProfileResponse


class NoRoleMeResponse(DTO):
    role: Literal[None] = None


MeResponse = Annotated[
    Union[CustomerMeResponse, VendorMeResponse, NoRoleMeResponse],
    Field(discriminator="role"),
]


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
    email: str
    raw_password: str
    password_reset_otp: str


class RefreshData(BaseModel):
    refresh_token: str | None = None


class LoginAccount(BaseModel):
    email: EmailStr
    raw_password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class AccountConfirmation(BaseModel):
    account_id: UUID
    confirm_code: str


class CreateAccountRequest(BaseModel):
    email: EmailStr
    raw_password: str


class ChangeEmailRequest(DTO):
    email: EmailStr


class ConfirmEmailChangeRequest(DTO):
    otp_code: str
