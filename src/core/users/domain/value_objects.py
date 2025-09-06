from dataclasses import dataclass

from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.users.infrastructure.services.phone_normalizer import PhoneNormalizer


@dataclass(frozen=True)
class Fullname:
    first_name: str
    last_name: str
    patronymic: str

    def __post_init__(self):
        self._validate_required()

    @classmethod
    def from_dict(cls, fullname: dict):
        return cls(
            first_name=fullname.get("first_name"),
            last_name=fullname.get("last_name"),
            patronymic=fullname.get("patronymic")
        )

    def _validate_required(self):
        if not self.first_name and not self.last_name:
            raise ValueError("Имя и Фамилия обязательные поля!")


@dataclass(frozen=True)
class Email:
    email: str

    def __post_init__(self):
        self._validate_required()

    def _validate_required(self):
        if not self.email:
            raise ValueError("Email не может быть пустым!")


@dataclass(frozen=True)
class Phone:
    phone: str

    @classmethod
    def from_raw(cls, raw_phone: str) -> "Phone":
        normalized_phone = PhoneNormalizer.normalize(raw_phone)
        return cls(normalized_phone)


@dataclass(frozen=True)
class OrganizationFullname:
    organization_fullname: str

    def __post_init__(self):
        self._validate_required()

    def _validate_required(self):
        if not self.organization_fullname:
            raise ValueError("Наименование организации обязательное поле!")


@dataclass(frozen=True)
class IIN:
    iin: str

    def __post_init__(self):
        self._validate_format()

    def _validate_format(self):
        if not self.iin.isdigit():
            raise ValueError("ИИН содержит недопустимые символы!")


@dataclass(frozen=True)
class BIN:
    bin: str

    def __post_init__(self):
        pass

    def _validate_format(self):
        if not self.bin.isdigit():
            raise ValueError("БИН содержит недопустимые символы!")


@dataclass(frozen=True)
class Password:
    hashed_password: str

    @classmethod
    def from_raw(cls, raw_password: str):
        hashed_str = BcryptPasswordHasher.hash_password(raw_password)
        return cls(hashed_str)

    def matches(self, raw_password: str) -> bool:
        verify = BcryptPasswordHasher.verify_password(raw_password, self.hashed_password)
        return verify
