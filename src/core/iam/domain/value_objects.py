from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        self.validate_required()
        self.validate_format()

    def validate_required(self):
        if not self.value:
            raise ValueError("Email обязателен")

    def validate_format(self):
        email_format = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_format, self.value):
            raise ValueError("Неправильный формат email")


@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self):
        if self.value is None:
            return
        self.validate()

    def validate(self):
        pattern = r"^\+77[0-9]\d{8}$"
        if not re.match(pattern, self.value):
            raise ValueError("Неправильный формат номера телефона")


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        self.validate_required()

    def validate_required(self):
        if not self.value:
            raise ValueError("Пароль обязателен")

