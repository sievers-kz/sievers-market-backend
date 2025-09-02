import uuid
from dataclasses import dataclass
from typing import Union

from src.core.users.domain.enums import UserRoleEnum, BusinessTypeEnum
from src.core.users.domain.value_objects import Fullname, Email, Phone, OrganizationFullname, IIN, BIN, Password


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
    password: Password
