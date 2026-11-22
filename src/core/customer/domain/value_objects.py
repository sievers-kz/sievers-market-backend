import re
from dataclasses import dataclass

from src.core.customer.domain.exceptions import (
    FullnameRequiredError,
    InvalidFullnameFormatError,
)


@dataclass(frozen=True)
class Fullname:
    last_name: str
    first_name: str
    patronymic: str | None = None

    def __post_init__(self):
        self.validate_required_fields()
        self.validate_fields_format()

    def validate_required_fields(self):
        if not self.first_name:
            raise FullnameRequiredError(field="first_name")
        if not self.last_name:
            raise FullnameRequiredError(field="last_name")

    def validate_fields_format(self):
        fullname_format = r"^[a-zA-Zа-яА-ЯёЁӘәҒғҚқҢңӨөҰұҮүҺһІі\s-]+$"
        if not re.match(fullname_format, self.first_name):
            raise InvalidFullnameFormatError(field="first_name")
        if not re.match(fullname_format, self.last_name):
            raise InvalidFullnameFormatError(field="last_name")
        if self.patronymic and not re.match(fullname_format, self.patronymic):
            raise InvalidFullnameFormatError(field="patronymic")
