from src.core.iam.domain.exceptions import (
    AccountAlreadyExistsError,
    AccountNotFoundError,
    CompromisedPasswordError,
    EmailChangeRequestNotFoundError,
    EmailRequiredError,
    InvalidEmailFormatError,
    InvalidLoginCredentialsError,
    InvalidOTPCodeError,
    InvalidPasswordError,
    InvalidTokenError,
    InvalidTokenTypeError,
    OTPCooldownError,
    PasswordMismatchError,
    PasswordRequiredError,
    RefreshTokenMissingError,
    TokenExpiredError,
)
from src.core.shared.presentation.documentation import RouteDocs

GET_ME_DOC = RouteDocs(
    operation_id="getMe",
    summary="Получить текущего пользователя",
    description="""
        Возвращает профиль аутентифицированного пользователя:
        * `Customer` - Покупатель
        * `Vendor` - Продавец
        * `None` - Если онбординг еще не пройден.
    """,
    responses=(
        AccountNotFoundError,
        InvalidTokenError,
        TokenExpiredError,
        InvalidTokenTypeError,
    ),
)

CREATE_NEW_USER_DOC = RouteDocs(
    operation_id="createNewUser",
    summary="Регистрация нового аккаунта",
    description="""
        Создает аккаунт по email и паролю.
        Пароль проверяется на вхождение в базу скомпроментированных (`Bloom Filter`).
        После создания на email отправляется код подтверждения.
    """,
    responses=(
        AccountAlreadyExistsError,
        CompromisedPasswordError,
        EmailRequiredError,
        InvalidEmailFormatError,
        PasswordRequiredError,
        InvalidPasswordError,
    ),
)

CONFIRM_ACCOUNT_DOC = RouteDocs(
    operation_id="confirmAccount",
    summary="Подтверждение аккаунта по коду",
    description="""
        Подтверждает регистрацию аккаунта одноразовым кодом, отправленным на email.
        В зависимости от клиента:
        * `Web` - Выставляет httpOnly-Cookie сессии
        * `Mobile` - Возвращает пару токенов в теле ответа.
    """,
    responses=(InvalidOTPCodeError,),
)

RESEND_CONFIRMATION_CODE_DOC = RouteDocs(
    operation_id="resendConfirmationCode",
    summary="Повторная отправка кода подтверждения",
    description="""
        Генерирует и отправляет новый код подтверждения на email аккаунта взамен
        истёкшего или утерянного.
    """,
    responses=(OTPCooldownError,),
)

LOGIN_USER_DOC = RouteDocs(
    operation_id="loginUser",
    summary="Вход по email и паролю",
    description="""
        Аутентифицирует пользователя.
        * `Web` - Для Web-клиента выставляет httpOnly-Cookie (`access` & `refresh`)
        * `Mobile` - Для мобильного клиента возвращает токены в JSON-теле.
    """,
    responses=(InvalidLoginCredentialsError,),
)

REFRESH_TOKEN_DOC = RouteDocs(
    operation_id="refreshToken",
    summary="Обновление пары токенов",
    description="""
        Выпускает новую пару `access` & `refresh` токенов по действующему refresh-токену
        (из cookie для web или из тела запроса для мобильного клиента).
    """,
    responses=(
        InvalidTokenError,
        InvalidTokenTypeError,
        TokenExpiredError,
        RefreshTokenMissingError,
    ),
)

LOGOUT_USER_DOC = RouteDocs(
    operation_id="logoutUser",
    summary="Выход из аккаунта",
    description="""
        Инвалидирует текущую сессию: отзывает refresh-токен и очищает httpOnly-cookie у web-клиента.
    """,
    responses=(),
)

REQUEST_FORGOT_PASSWORD_DOC = RouteDocs(
    operation_id="requestForgotPassword",
    summary="Запрос на восстановление пароля",
    description="""
        Отправляет на email одноразовый код для сброса пароля.
    """,
    responses=(OTPCooldownError,),
)

RESET_USER_PASSWORD_DOC = RouteDocs(
    operation_id="resetUserPassword",
    summary="Сброс пароля по коду",
    description="""
        Устанавливает новый пароль по коду восстановления, ранее отправленному на email.
    """,
    responses=(
        InvalidOTPCodeError,
        CompromisedPasswordError,
        InvalidPasswordError,
        PasswordRequiredError,
    ),
)

CHANGE_PASSWORD_DOC = RouteDocs(
    operation_id="changePassword",
    summary="Смена пароля",
    description="""
        Меняет пароль аутентифицированного пользователя. Требует ввода текущего пароля.
    """,
    responses=(
        InvalidTokenError,
        InvalidTokenTypeError,
        TokenExpiredError,
        PasswordRequiredError,
        InvalidPasswordError,
        CompromisedPasswordError,
        PasswordMismatchError,
    ),
)

REQUEST_EMAIL_CHANGE_DOC = RouteDocs(
    operation_id="requestEmailChange",
    summary="Запрос на смену email",
    description="""
        Инициирует смену email: отправляет код подтверждения на новый адрес,
        email аккаунта не меняется до подтверждения.
    """,
    responses=(
        InvalidTokenError,
        InvalidTokenTypeError,
        TokenExpiredError,
        AccountAlreadyExistsError,
        EmailRequiredError,
        InvalidEmailFormatError,
    ),
)

CONFIRM_EMAIL_CHANGE_DOC = RouteDocs(
    operation_id="confirmEmailChange",
    summary="Подтверждение смены email",
    description="""
        Подтверждает смену email одноразовым кодом, отправленным на новый адрес.
    """,
    responses=(
        EmailChangeRequestNotFoundError,
        InvalidOTPCodeError,
        InvalidTokenError,
        InvalidTokenTypeError,
        TokenExpiredError,
    ),
)
