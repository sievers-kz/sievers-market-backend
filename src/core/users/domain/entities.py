import uuid
from dataclasses import dataclass
from datetime import datetime
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
    profile: Union["IndividualUserEntity", "BusinessUserEntity"]
    authentication: "UserAuthEntity"


@dataclass
class IndividualUserEntity:
    pass


@dataclass
class BusinessUserEntity:
    business_type: BusinessTypeEnum
    organization_fullname: OrganizationFullname
    iin: IIN
    bin: BIN


@dataclass
class UserAuthEntity:
    password: HashedPassword


@dataclass
class AuthTokenAggregate:
    id: uuid.UUID
    user_id: uuid.UUID
    token_type: TokenTypeEnum
    token_value: str
    is_revoked: bool
    expires_at: datetime
