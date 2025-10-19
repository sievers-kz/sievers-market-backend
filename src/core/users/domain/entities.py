import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Union

from src.core.users.domain.enums import UserRoleEnum, BusinessTypeEnum
from src.core.users.domain.exceptions.exception_classes import EmailAlreadyConfirmedError
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
            raise EmailAlreadyConfirmedError(code="email_already_confirmed")
        self.is_active = True

    def change_password(self, new_raw_password: str):
        new_hashed_password = HashedPassword.from_raw(raw_password=new_raw_password)
        self.authentication.password = new_hashed_password


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



