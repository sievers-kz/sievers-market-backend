import re
from dataclasses import dataclass


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
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")

    def validate_fields_format(self):
        fullname_format = r"^[a-zA-Zа-яА-ЯёЁ\s-]+$"
        if not re.match(fullname_format, self.first_name):
            raise ValueError("Invalid first name format")
        if not re.match(fullname_format, self.last_name):
            raise ValueError("Invalid last name format")
        if self.patronymic and not re.match(fullname_format, self.patronymic):
            raise ValueError("Invalid patronymic format")


@dataclass(frozen=True)
class CompanyName:
    value: str

    def __post_init__(self):
        self.validate_required()
        self.validate_length()

    def validate_required(self):
        if not self.value:
            raise ValueError("Legal name is required")

    def validate_length(self):
        if len(self.value) > 100:
            raise ValueError("Legal name is too long")


@dataclass(frozen=True)
class TaxID:
    value: str

    def __post_init__(self):
        self.validate_required()
        self.validate_format()
        self.validate_length()

    def validate_required(self):
        if not self.value:
            raise ValueError("Tax ID is required")

    def validate_length(self):
        if len(self.value) != 12:
            raise ValueError("Tax ID must be 12 digits long")

    def validate_format(self):
        if not re.match(r"^\d{12}$", self.value):
            raise ValueError("Tax ID must be a number")
