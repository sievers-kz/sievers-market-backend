from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        self.validate_required()
        self.validate_length()

    @classmethod
    def create(cls, brand_name: str, model: str | None = None) -> "Title":
        raw_value = f"{brand_name} {model}".strip() if model else brand_name
        return cls(value=raw_value)

    def validate_required(self):
        if not self.value:
            raise ValueError("Заголовок обязательное поле")

    def validate_length(self):
        if len(self.value) > 50:
            raise ValueError("Заголовок не должен превышать 50 символов")


@dataclass(frozen=True)
class Price:
    value: int

    def __post_init__(self):
        self.validate_required()
        self.validate_range()

    def validate_required(self):
        if not self.value:
            raise ValueError("Цена обязательное поле")

    def validate_range(self):
        if self.value < 0:
            raise ValueError("Цена не может быть отрицательной")


@dataclass(frozen=True)
class YearOfIssue:
    value: int

    def __post_init__(self):
        self.validate_required()
        self.validate_range()

    def validate_required(self):
        if not self.value:
            raise ValueError("Год выпуска обязательное поле")

    def validate_range(self):
        current_year = datetime.now().year
        if self.value < 1900:
            raise ValueError("Год выпуска не может быть менье 1900")
        if self.value > current_year:
            raise ValueError(f"Год выпуска не может превышать текущий ({current_year})")


@dataclass(frozen=True)
class Description:
    value: str

    def __post_init__(self):
        self.validate_length()

    def validate_length(self):
        if len(self.value) > 3000:
            raise ValueError("Описание не должно превышать 3000 символов")
