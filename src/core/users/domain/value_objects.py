import re
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TypeVar, Generic

from src.core.users.infrastructure.services.phone_normalizer import PhoneNormalizer
from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher


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
            raise ValueError("Имя обязательное поле!")
        if not last_name:
            raise ValueError("Фамилия обязательное поле!")
        return cls(first_name=first_name, last_name=last_name, patronymic=patronymic)

    def _validate(self):
        fullname_format = r"^[а-яА-ЯёЁ\s-]+$"
        if not re.match(fullname_format, self.first_name):
            raise ValueError("Имя должно содержать только кириллицу!")
        if not re.match(fullname_format, self.last_name):
            raise ValueError("Фамилия должна содержать только кириллицу!")
        if self.patronymic and not re.match(fullname_format, self.patronymic):
            raise ValueError("Отчество должно содержать только кириллицу!")


@dataclass(frozen=True)
class Email(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_email: str) -> "Email":
        if not raw_email:
            raise ValueError("Email обязательное поле!")

        normalize = raw_email.lower().strip()
        return cls(value=normalize)

    def _validate(self):
        email_format = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_format, self.value):
            raise ValueError("Некорректный формат email адреса!")


@dataclass(frozen=True)
class Phone(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_phone: str | None) -> "Phone":
        if not raw_phone:
            return cls(value=None)

        normalize = PhoneNormalizer.normalize(raw_phone)
        return cls(value=normalize)

    def _validate(self):
        pass


@dataclass(frozen=True)
class OrganizationFullname(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_organization_fullname: str) -> "OrganizationFullname":
        if not raw_organization_fullname:
            raise ValueError("Наименование организации обязательное поле!")

        normalize = raw_organization_fullname.strip()
        return cls(value=normalize)

    def _validate(self):
        pass


@dataclass(frozen=True)
class IIN(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_iin: str | None) -> "IIN":
        if not raw_iin:
            return cls(value=None)

        normalize = raw_iin.strip()
        return cls(value=normalize)

    def _validate(self):
        if not self.value.isdigit():
            raise ValueError("ИИН должен содержать только цифры!")
        if len(self.value) != 12:
            raise ValueError("Длина ИИН должна быть равной 12!")


@dataclass(frozen=True)
class BIN(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_bin: str | None) -> "BIN":
        if not raw_bin:
            return cls(value=None)

        normalize = raw_bin.strip()
        return cls(value=normalize)

    def _validate(self):
        if not self.value.isdigit():
            raise ValueError("БИН должен содержать только цифры!")
        if len(self.value) != 12:
            raise ValueError("Длина БИН должна быть равной 12!")


@dataclass(frozen=True)
class HashedPassword:
    hashed_password: str

    @classmethod
    def from_raw(cls, raw_password: str) -> "HashedPassword":
        if not raw_password:
            raise ValueError("Пароль обязательное поле!")

        hashed = BcryptPasswordHasher.hash_password(raw_password)
        return cls(hashed_password=hashed)

    @classmethod
    def from_hash(cls, hashed_password: str) -> "HashedPassword":
        if not hashed_password:
            raise ValueError("Хэшированный пароль не может быть пустым!")
        return cls(hashed_password=hashed_password)

    def matches(self, raw_password: str):
        return BcryptPasswordHasher.verify_password(raw_password, self.hashed_password)