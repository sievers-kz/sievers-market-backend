from src.core.shared.domain.exceptions import NotFoundError, ValidationError


class CustomerNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(message="Не удалось найти профиль покупателя")


class FullnameRequiredError(ValidationError):
    def __init__(self, field: str):
        super().__init__(
            message="Обязательное поле не заполнено", details={"field": field}
        )


class InvalidFullnameFormatError(ValidationError):
    def __init__(self, field: str):
        super().__init__(message="Неверный формат поля", details={"field": field})
