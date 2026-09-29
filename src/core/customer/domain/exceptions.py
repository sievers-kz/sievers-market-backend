from src.core.shared.domain.exceptions import (
    AccessDeniedError,
    NotFoundError,
    ValidationError,
)


class CustomerNotFoundError(NotFoundError):
    message = "Не удалось найти профиль покупателя"
    error_code = "customer_not_found_error"


class FullnameRequiredError(ValidationError):
    message = "Обязательное поле не заполнено"
    error_code = "fullname_required_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class InvalidFullnameFormatError(ValidationError):
    message = "Неверный формат поля"
    error_code = "invalid_fullname_format_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class CustomerProfileRequiredError(AccessDeniedError):
    message = "Доступ запрещен. Необходимо иметь профиль покупателя"
    error_code = "customer_profile_required_error"
