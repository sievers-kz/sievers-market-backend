import datetime

from src.core.users.domain.value_objects import ValueObject


class Title(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_value: str | None) -> "Title":
        return cls(value=raw_value)

    def _validate(self):
        if self.value is not None:
            if len(self.value) > 50:
                raise ValueError("Заголовок не должен превышать 50 символов")
            if not isinstance(self.value, str):
                raise ValueError("Заголовок должен быть строкой")


class Price(ValueObject[int]):
    @classmethod
    def from_raw(cls, raw_value: int | None) -> "Price":
        return cls(value=int(raw_value))

    def _validate(self):
        if self.value is not None:
            if self.value < 0:
                raise ValueError("Слишком низкая цена")
            if not isinstance(self.value, (int, float)):
                raise ValueError("Цена должна быть числом")


class Model(ValueObject[str]):
    @classmethod
    def from_raw(cls, raw_value: str | None) -> "Model":
        return cls(value=raw_value)

    def _validate(self):
        if self.value is not None:
            if len(self.value) > 50:
                raise ValueError("Длина модели не должна превышать 50 символов")


class YearOfIssue(ValueObject[int]):
    @classmethod
    def from_raw(cls, raw_value: int | None) -> "YearOfIssue":
        return cls(value=int(raw_value))

    def _validate(self):
        if self.value is not None:
            if self.value < 1900:
                raise ValueError("Год не может быть меньше 1900")
            if self.value > datetime.datetime.now().year:
                raise ValueError("Год не может быть больше нынешнего")
