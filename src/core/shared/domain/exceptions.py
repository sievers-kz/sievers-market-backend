class DomainException(Exception):
    status_code: int = 500
    error_code: str = "internal_error"
    message: str = "Внутренняя ошибка сервера"

    def __init__(
        self,
        message: str | None = None,
        metadata: dict | None = None,
    ):
        self.message = message or self.message
        self.metadata = metadata or {}
        super().__init__(message)


class TooManyRequestsError(DomainException):
    status_code = 429


class NotFoundError(DomainException):
    status_code = 404


class UnauthorizedError(DomainException):
    status_code = 401


class AlreadyExistsError(DomainException):
    status_code = 409


class ConflictError(DomainException):
    status_code = 409


class ValidationError(DomainException):
    status_code = 422


class RulesError(DomainException):
    status_code = 400


class AccessDeniedError(DomainException):
    status_code = 403


class InvalidPhoneFormatError(ValidationError):
    message = "Некорректный формат номера телефона"
    error_code = "invalid_phone_format_error"
