import datetime
import re
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.domain.exceptions import (
    ContactFullnameFormatError,
    ContactFullnameRequiredError,
    InvalidLogotypeSizeError,
    InvalidTaxNumberError,
)


@dataclass(frozen=True)
class ContactFullname:
    contact_last_name: str
    contact_first_name: str
    contact_patronymic: str | None = None

    def __post_init__(self):
        self.validate_required_fields()
        self.validate_fields_format()

    def validate_required_fields(self):
        if not self.contact_last_name:
            raise ContactFullnameRequiredError(field="Фамилия")
        if not self.contact_first_name:
            raise ContactFullnameRequiredError(field="Имя")

    def validate_fields_format(self):
        fullname_format = r"^[a-zA-Zа-яА-ЯёЁ\s-]+$"
        if not re.match(fullname_format, self.contact_last_name):
            raise ContactFullnameFormatError(field="Фамилия")
        if not re.match(fullname_format, self.contact_first_name):
            raise ContactFullnameFormatError(field="Имя")
        if self.contact_patronymic and not re.match(
            fullname_format, self.contact_patronymic
        ):
            raise ContactFullnameFormatError(field="Отчество")


@dataclass(frozen=True)
class TaxID:
    value: str
    type: LegalForm

    def __post_init__(self):
        self.validate_format()
        if not self._check_rk_checksum():
            raise InvalidTaxNumberError()
        self.validate_tax_by_type()

    def validate_format(self):
        if not self.value.isdigit() or len(self.value) != 12:
            raise InvalidTaxNumberError()

    def validate_tax_by_type(self):
        if self.type == LegalForm.IE:
            self._validate_iin_structure()
        else:
            self._validate_bin_structure()

    def _validate_iin_structure(self) -> None:
        birth_date_str = self.value[0:6]
        try:
            datetime.datetime.strptime(birth_date_str, "%y%m%d")
        except ValueError:
            raise InvalidTaxNumberError()

        if self.value[6] not in ("1", "2", "3", "4", "5", "6"):
            raise InvalidTaxNumberError()

    def _validate_bin_structure(self) -> None:
        month = int(self.value[2:4])
        if month < 1 or month > 12:
            raise InvalidTaxNumberError()

        if self.value[4] not in ("4", "5", "6"):
            raise InvalidTaxNumberError()

    def _check_rk_checksum(self) -> bool:
        """Алгоритм проверки контрольного разряда ИИН/БИН Республики Казахстан"""
        digits = [int(char) for char in self.value]

        weights_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        checksum = sum(d * w for d, w in zip(digits[:11], weights_1)) % 11

        if checksum == 10:
            weights_2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
            checksum = sum(d * w for d, w in zip(digits[:11], weights_2)) % 11

            if checksum == 10:
                return False

        return digits[11] == checksum


@dataclass(frozen=True)
class Logotype:
    MAX_SIZE_BYTES = 2 * 1024 * 1024
    media_id: UUID
    media_type: str
    media_size: int

    def __post_init__(self):
        if self.media_size > self.MAX_SIZE_BYTES:
            raise InvalidLogotypeSizeError()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Logotype":
        return cls(
            media_id=UUID(str(data["media_id"])),
            media_type=str(data["media_type"]),
            media_size=int(data["media_size"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "media_id": str(self.media_id),
            "media_type": self.media_type,
            "media_size": self.media_size,
        }
