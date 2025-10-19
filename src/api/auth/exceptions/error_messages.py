from fastapi import status

from src.core.auth.domain.exceptions.exception_classes import TokenCryptographyError, TokenStateError
from src.core.auth.domain.exceptions.exception_classes import InvalidCredentialsError


AUTH_ERROR_MESSAGES = {
    "invalid_login_credentials": "Неправильный email или пароль",
    "token_cryptography_error": "Сессия недействительна. Пожалуйста, войдите заново",
    "token_state_error": "Сессия недействительна. Пожалуйста, войдите заново",
}


AUTH_HTTP_STATUS_MAP = {
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
    TokenCryptographyError: status.HTTP_401_UNAUTHORIZED,
    TokenStateError: status.HTTP_401_UNAUTHORIZED,
}

