import uuid
from abc import ABC, abstractmethod
from datetime import timedelta, datetime, timezone

import jwt

from src.api.auth.auth_dto import AuthTokenDTO
from src.core.auth.domain.enums import TokenTypeEnum

from src.core.auth.infrastructure.exceptions.exception_classes import (
    TokenExpiredError,
    InvalidTokenError,
    TokenGeneratorService
)


class AbstractTokenService(ABC):
    @abstractmethod
    def create_auth_token(self, user_id: uuid.UUID, token_type: TokenTypeEnum) -> AuthTokenDTO:
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str, expected_type: TokenTypeEnum) -> dict:
        raise NotImplementedError


class PyJWTTokenService(AbstractTokenService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_lifetime: timedelta,
        refresh_token_lifetime: timedelta,
        email_token_lifetime: timedelta,
        password_reset_token_lifetime: timedelta
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm

        self._lifetimes = {
            TokenTypeEnum.ACCESS_TOKEN: access_token_lifetime,
            TokenTypeEnum.REFRESH_TOKEN: refresh_token_lifetime,
            TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN: email_token_lifetime,
            TokenTypeEnum.PASSWORD_RESET_TOKEN: password_reset_token_lifetime
        }

    def create_auth_token(self, user_id: uuid.UUID, token_type: TokenTypeEnum) -> AuthTokenDTO:
        lifetime = self._lifetimes.get(token_type)
        expires_at = datetime.now(timezone.utc) + lifetime
        payload = {"sub": str(user_id), "exp": expires_at, "token_type": token_type.value}
        token_str = jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)

        return AuthTokenDTO(
            token_type=token_type,
            token_value=token_str,
            expires_at=expires_at,
            is_revoked=False
        )

    def verify_token(self, token: str, expected_type: TokenTypeEnum) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            token_type = payload.get("token_type")
            if not token_type or token_type != expected_type.value:
                raise InvalidTokenError(code="invalid_token_error")

            return payload

        except jwt.ExpiredSignatureError as exc:
            raise TokenExpiredError(
                code="token_expired_error",
                details=str(exc),
            ) from exc

