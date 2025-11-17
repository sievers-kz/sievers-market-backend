import re
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TypeVar, Generic

from src.core.users.domain.enums import DocumentTypeEnum, BusinessTypeEnum
from src.core.users.domain.exceptions.exception_classes import MissingRequiredFieldError, InvalidInputError


TValueObject = TypeVar("TValueObject")


@dataclass(frozen=True)
class ValueObject(Generic[TValueObject], ABC):
    value: TValueObject | None

    def __post_init__(self):
        if self.value is None:
            return

        self._validate()

    @abstractmethod
    def _validate(self):
        raise NotImplementedError


@dataclass(frozen=True)
class Fullname:
    first_name: str
    last_name: str
    patronymic: str | None

    def __post_init__(self):
        self._validate()

    @classmethod
    def from_raw(cls, first_name: str, last_name: str, patronymic: str | None) -> "Fullname":
        if not first_name:
            raise MissingRequiredFieldError(
                code="missing_required_field",
                context={
                    "field": "first_name",
                    "verbose_name": "Имя"
                }
            )

        if not last_name:
            raise MissingRequiredFieldError(
                code="missing_required_field",
                context={
                    "field": "last_name",
                    "verbose_name": "Фамилия"
                }
            )

        return cls(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )

    def _validate(self):
        fullname_format = r"^[а-яА-ЯёЁ\s-]+$"

        if not re.match(fullname_format, self.first_name):
            raise InvalidInputError(
                code="invalid_fullname_format",
                context={
                    "field": "first_name",
                    "verbose_name": "Имя"
                }
            )

        if not re.match(fullname_format, self.last_name):
            raise InvalidInputError(
                code="invalid_fullname_format",
                context={
                    "field": "last_name",
                    "verbose_name": "Фамилия"
                }
            )

        if self.patronymic and not re.match(fullname_format, self.patronymic):
            raise InvalidInputError(
                code="invalid_fullname_format",
                context={
                    "field": "patronymic",
                    "verbose_name": "Отчество"
                }
            )


@dataclass(frozen=True)
class Email(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_email: str) -> "Email":
        if not raw_email:
            raise MissingRequiredFieldError(
                code="missing_required_field",
                context={
                    "field": "email",
                    "verbose_name": "Email"
                }
            )

        normalize = raw_email.lower().strip()
        return cls(value=normalize)

    def _validate(self):
        email_format = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_format, self.value):
            raise InvalidInputError(
                code="invalid_email_format",
                context={
                    "field": "email",
                    "verbose_name": "Email",
                    "value": self.value
                }
            )


@dataclass(frozen=True)
class Phone(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_phone: str | None) -> "Phone":
        if not raw_phone:
            return cls(value=None)
        return cls(value=raw_phone)

    def _validate(self):
        pattern = r"^\+77[0-9]\d{8}$"
        if not re.match(pattern, self.value):
            raise InvalidInputError(
                code="invalid_phone_format",
                context={
                    "field": "phone",
                    "verbose_name": "Номер телефона",
                    "value": self.value
                }
            )


@dataclass(frozen=True)
class OrganizationFullname(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_organization_fullname: str) -> "OrganizationFullname":
        if not raw_organization_fullname:
            raise MissingRequiredFieldError(
                code="missing_required_field",
                context={
                    "field": "organization_fullname",
                    "verbose_name": "Наименование организации"
                }
            )

        normalize = raw_organization_fullname.strip()
        return cls(value=normalize)

    def _validate(self):
        pattern = (
            r"^[A-Za-zА-Яа-яӘәІіҢңҒғҮүҰұҚқӨөҺһ0-9№]"
            r"[A-Za-zА-Яа-яӘәІіҢңҒғҮүҰұҚқӨөҺһ0-9\s.&'\"(),/#\-№]*$"
        )
        if not re.match(pattern, self.value):
            raise InvalidInputError(
                code="invalid_org_name_format",
                context={
                    "field": "organization_fullname",
                    "verbose_name": "Наименование организации"
                }
            )


class DocumentValue(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_value: str) -> "DocumentValue":
        if not raw_value:
            raise MissingRequiredFieldError(
                code="missing_required_field",
                context={
                    "field": "document_value",
                    "verbose_name": "Уникальный номер документа"
                }
            )
        return cls(value=raw_value)

    def _validate(self):
        if not self.value.isdigit():
            raise InvalidInputError(
                code="invalid_document_format",
                context={
                    "field": "document_value",
                    "verbose_name": "Уникальный номер документа"
                }
            )

        if len(self.value) != 12:
            raise InvalidInputError(
                code="invalid_document_format",
                context={
                    "field": "document_value",
                    "verbose_name": "Уникальный номер документа"
                }
            )
