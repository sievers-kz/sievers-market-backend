from dataclasses import dataclass
import re

from src.core.iam.domain.exceptions import EmailRequiredError, InvalidEmailFormatError, PasswordRequiredError


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        self.validate_required()
        self.validate_format()

    def validate_required(self):
        if not self.value:
            raise EmailRequiredError()

    def validate_format(self):
        email_format = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_format, self.value):
            raise InvalidEmailFormatError()


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        self.validate_required()

    def validate_required(self):
        if not self.value:
            raise PasswordRequiredError()



