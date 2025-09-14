import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Union

from src.core.users.domain.enums import UserRoleEnum, BusinessTypeEnum, TokenTypeEnum
from src.core.users.domain.value_objects import Fullname, Email, Phone, OrganizationFullname, IIN, BIN, HashedPassword


@dataclass
class UserAggregate:
    id: uuid.UUID
    role: UserRoleEnum
    fullname: Fullname
    email: Email
    phone: Phone
    is_active: bool
    profile: Union["IndividualUserEntity", "BusinessUserEntity"]
    authentication: "UserAuthEntity"

    def confirm_email(self):
        if self.is_active:
            raise ValueError("Email уже подтвержден!")
        self.is_active = True


@dataclass
class IndividualUserEntity:
    id: uuid.UUID


@dataclass
class BusinessUserEntity:
    id: uuid.UUID
    business_type: BusinessTypeEnum
    organization_fullname: OrganizationFullname
    iin: IIN
    bin: BIN


@dataclass
class UserAuthEntity:
    id: uuid.UUID
    password: HashedPassword


@dataclass
class AuthTokenAggregate:
    id: uuid.UUID
    user_id: uuid.UUID
    token_type: TokenTypeEnum
    token_value: str
    is_revoked: bool
    expires_at: datetime

    def is_expired(self):
        current_time = datetime.now(timezone.utc)
        return current_time > self.expires_at
