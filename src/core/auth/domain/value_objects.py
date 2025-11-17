from dataclasses import dataclass
from src.core.users.domain.exceptions.exception_classes import MissingRequiredFieldError


@dataclass(frozen=True)
class HashedPassword:
    hashed_password: str

    @classmethod
    def from_raw(cls, raw_password: str) -> "HashedPassword":
        if not raw_password:
            raise MissingRequiredFieldError(
                code="missing_required_field",
                context={
                    "field": "password",
                    "verbose_name": "Пароль"
                }
            )

        return cls(hashed_password=raw_password)

    @classmethod
    def from_hash(cls, hashed_password: str) -> "HashedPassword":
        if not hashed_password:
            raise ValueError("Хэшированный пароль не может быть пустым!")
        return cls(hashed_password=hashed_password)

