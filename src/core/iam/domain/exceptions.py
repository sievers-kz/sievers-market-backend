from src.core.shared.domain.exceptions import (
    ConflictError,
    NotFoundError,
    RulesError,
    TooManyRequestsError,
    UnauthorizedError,
    ValidationError,
)


class AccountNotFoundError(NotFoundError):
    message = "Аккаунт не найден"
    error_code = "account_not_found_error"


class AccountAlreadyExistsError(ConflictError):
    message = "Такой аккаунт уже зарегистрирован"
    error_code = "account_already_exists_error"


class AccountNotConfirmedError(UnauthorizedError):
    message = "Аккаунт все еще не подтвержден"
    error_code = "account_not_confirmed_error"


class AccountAlreadyConfirmedError(ConflictError):
    message = "Аккаунт уже был подтвержден"
    error_code = "account_already_confirmed_error"


class OTPCooldownError(TooManyRequestsError):
    message = "Подождите перед повторной отправкой кода"
    error_code = "otp_cooldown_error"


class InvalidOTPCodeError(RulesError):
    message = "Некорректный код подтверждения"
    error_code = "invalid_otp_code_error"


class InvalidLoginCredentialsError(UnauthorizedError):
    message = "Неправильный email или пароль"
    error_code = "invalid_login_credentials_error"


class EmailChangeRequestNotFoundError(RulesError):
    message = "Запрос на смену email истек или не найден"
    error_code = "email_change_request_not_found_error"


class PasswordMismatchError(RulesError):
    message = "Введенные вами пароли не совпадают"
    error_code = "password_mismatch_error"


class EmailRequiredError(ValidationError):
    message = "Email обязателен"
    error_code = "email_required_error"


class InvalidEmailFormatError(ValidationError):
    message = "Некорректный формат email"
    error_code = "invalid_email_format_error"


class PasswordRequiredError(ValidationError):
    message = "Пароль обязателен"
    error_code = "password_required_error"


class InvalidPasswordError(ValidationError):
    message = "Некорректный формат пароля"
    error_code = "invalid_password_error"


class CompromisedPasswordError(RulesError):
    message = "Пароль слишком распространен. Придумайте другой"
    error_code = "compromised_password_error"


class InvalidTokenTypeError(UnauthorizedError):
    message = "Неверный тип токена"
    error_code = "invalid_token_type_error"


class TokenExpiredError(UnauthorizedError):
    message = "Сессия истекла. Войдите снова"
    error_code = "token_expired_error"


class InvalidTokenError(UnauthorizedError):
    message = "Недействительный токен"
    error_code = "invalid_token_error"


class RefreshTokenMissingError(UnauthorizedError):
    message = "Рефреш-токен не найден в запросе"
    error_code = "refresh_token_missing_error"
