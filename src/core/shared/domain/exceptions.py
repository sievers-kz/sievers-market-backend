class DomainException(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundError(DomainException):
    pass


class UnauthorizedError(DomainException):
    pass


class AlreadyExistsError(DomainException):
    pass


class ValidationError(DomainException):
    pass


class RulesError(DomainException):
    pass


class InvalidPhoneFormatError(ValidationError):
    def __init__(self):
        super().__init__(message="Некорректный формат номера телефона")
