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


