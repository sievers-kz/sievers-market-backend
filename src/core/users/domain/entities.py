import uuid
from dataclasses import dataclass
from typing import Optional

from src.core.shared.domain.entities import AggregateRoot, Entity
from src.core.users.domain.enums import UserRoleEnum, BusinessTypeEnum, DocumentTypeEnum
from src.core.users.domain.exceptions.exception_classes import EmailAlreadyConfirmedError, InvalidInputError
from src.core.users.domain.value_objects import Email, Phone, Fullname, OrganizationFullname, DocumentValue


@dataclass(frozen=False)
class User(AggregateRoot):
    id: uuid.UUID
    role: UserRoleEnum
    email: Email
    phone: Phone
    is_active: bool
    profile: "UserProfile"
    business_details: Optional["BusinessDetails"] = None

    def confirm_user(self):
        if self.is_active:
            raise EmailAlreadyConfirmedError(code="email_already_confirmed")
        self.is_active = True

    def change_fullname(self, first_name: str, last_name: str, patronymic: str | None):
        self.profile.change_fullname(first_name=first_name, last_name=last_name, patronymic=patronymic)

    def change_email(self, raw_email: str):
        self.email = Email.from_raw(raw_email=raw_email)

    def change_phone(self, raw_phone: str):
        self.phone = Phone.from_raw(raw_phone=raw_phone)

    def change_organization_fullname(self, raw_organization_fullname: str):
        self.business_details.change_organization_fullname(raw_organization_fullname=raw_organization_fullname)

    def change_business_details_document_value(self, raw_document_value: str):
        self.business_details.change_document_value(raw_document_value=raw_document_value)

    def change_avatar(self, avatar_url: str):
        self.profile.change_avatar(avatar_url=avatar_url)


@dataclass(frozen=False)
class UserProfile(Entity):
    id: uuid.UUID
    user_id: uuid.UUID
    fullname: Fullname
    avatar_url: str | None = None

    def change_fullname(self, first_name: str, last_name: str, patronymic: str | None):
        self.fullname = Fullname.from_raw(first_name=first_name, last_name=last_name, patronymic=patronymic)

    def change_avatar(self, avatar_url: str):
        self.avatar_url = avatar_url


@dataclass(frozen=False)
class BusinessDetails(Entity):
    id: uuid.UUID
    user_id: uuid.UUID
    business_type: BusinessTypeEnum
    organization_fullname: OrganizationFullname
    document_type: DocumentTypeEnum
    document_value: DocumentValue

    def __post_init__(self):
        self._validate_document_consistency()

    def _validate_document_consistency(self):
        if self.business_type == BusinessTypeEnum.IP:
            if self.document_type != DocumentTypeEnum.IIN:
                raise InvalidInputError(
                    code="invalid_document_type_for_individual",
                    context={
                        "field": "document_type",
                        "verbose_name": "Тип документа",
                    }
                )

        if self.business_type == BusinessTypeEnum.TOO:
            if self.document_type != DocumentTypeEnum.BIN:
                raise InvalidInputError(
                    code="invalid_document_type_for_too",
                    context={
                        "field": "document_type",
                        "verbose_name": "Тип документа"
                    }
                )

    def change_organization_fullname(self, raw_organization_fullname: str):
        self.organization_fullname = OrganizationFullname.from_raw(
            raw_organization_fullname=raw_organization_fullname
        )

    def change_document_value(self, raw_document_value: str):
        self.document_value = DocumentValue.from_raw(raw_value=raw_document_value)
