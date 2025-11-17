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


@dataclass(frozen=False)
class UserProfile(Entity):
    id: uuid.UUID
    user_id: uuid.UUID
    fullname: Fullname
    avatar_url: str | None = None


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

