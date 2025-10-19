from fastapi import status

from src.core.users.application.exceptions.exception_classes import ServiceUnavailableError, InternalServerError

from src.core.users.domain.exceptions.exception_classes import (
    UserAlreadyExistsError,
    MissingRequiredFieldError,
    InvalidInputError,
    EmailNotConfirmedError,
    InvalidEmailConfirmationCodeError,
    ConfirmationCodeExpiredError
)


USER_ERROR_MESSAGES = {
    # DOMAIN
    "user_already_exists": "Такой {verbose_name} уже зарегистрирован",

    "email_not_confirmed": "Ваш email адрес не подтвержден. Пожалуйста, проверьте почту для завершения регистрации",
    "invalid_confirmation_code": "Неправильная ссылка подтверждения электронной почты. Запросите новое письмо.",
    "confirmation_code_expired": "Ссылка для подтверждения электронной почты истекла. Запросите новую.",

    # DOMAIN VALUE OBJECTS
    "missing_required_field": "{verbose_name} обязательное поле",
    "invalid_fullname_format": "{verbose_name} должно быть написано на Русском или Казахском языках",
    "invalid_email_format": "{verbose_name} имеет некорректный формат. Пример: user@example.com",
    "invalid_phone_format": "{verbose_name} написан неправильно. Пример: +7(747)200-62-43",
    "invalid_identification_number_format.type": "{verbose_name} должен состоять из целых чисел",
    "invalid_identification_number_format.length": "{verbose_name} должен состоять из 12 целых цисел",

    # APPLICATION
    "service_unavailable_error": "Сервис временно недоступен. Пожалуйста, попробуйте позднее",
    "internal_server_error": "Технические неполадки. Пожалуйста, попробуйте позднее",
}


PYDANTIC_ERROR_MESSAGES = {
    "missing": "{verbose_name} обязательно для заполнения",
    "string_type": "{verbose_name} должно быть строкой",
    "int_type": "{verbose_name} должно быть целым числом",
}


USER_HTTP_STATUS_MAP = {
    UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    MissingRequiredFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    InvalidInputError: status.HTTP_422_UNPROCESSABLE_ENTITY,

    EmailNotConfirmedError: status.HTTP_401_UNAUTHORIZED,
    InvalidEmailConfirmationCodeError: status.HTTP_400_BAD_REQUEST,
    ConfirmationCodeExpiredError: status.HTTP_400_BAD_REQUEST,

    ServiceUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
    InternalServerError: status.HTTP_500_INTERNAL_SERVER_ERROR
}
