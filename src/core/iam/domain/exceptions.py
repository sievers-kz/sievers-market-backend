from src.core.shared.domain.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    RulesError,
    UnauthorizedError,
    ValidationError,
)


class AccountNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(message="Аккаунт не найден")


class AccountAlreadyExistsError(AlreadyExistsError):
    def __init__(self):
        super().__init__(message="Такой аккаунт уже зарегистрирован")


class AccountNotConfirmedError(UnauthorizedError):
    def __init__(self):
        super().__init__(message="Аккаунт все еще не подтвержден")


class AccountAlreadyConfirmedError(RulesError):
    def __init__(self):
        super().__init__(message="Аккаунт уже был подтвержден")


class OTPCooldownError(RulesError):
    def __init__(self):
        super().__init__(message="Подождите перед повторной отправкой кода")


class InvalidOTPCodeError(RulesError):
    def __init__(self):
        super().__init__(message="Некорректный код подтверждения")


class InvalidLoginCredentialsError(UnauthorizedError):
    def __init__(self):
        super().__init__(message="Неправильный email или пароль")


class EmailChangeRequestNotFoundError(RulesError):
    def __init__(self):
        super().__init__(message="Запрос на смену email истек или не найден")


class PasswordMismatchError(RulesError):
    def __init__(self):
        super().__init__(message="Введенные вами пароли не совпадают")


class EmailRequiredError(ValidationError):
    def __init__(self):
        super().__init__(message="Email обязателен")


class InvalidEmailFormatError(ValidationError):
    def __init__(self):
        super().__init__(message="Некорректный формат email")


class PasswordRequiredError(ValidationError):
    def __init__(self):
        super().__init__(message="Пароль обязателен")


class InvalidPasswordError(ValidationError):
    def __init__(self, message: str = "Некорректный формат пароля"):
        super().__init__(message=message)


class InvalidTokenTypeError(UnauthorizedError):
    def __init__(self):
        super().__init__("Неверный тип токена")


class TokenExpiredError(UnauthorizedError):
    def __init__(self):
        super().__init__("Сессия истекла, войдите снова")


class InvalidTokenError(UnauthorizedError):
    def __init__(self):
        super().__init__("Недействительный токен")
