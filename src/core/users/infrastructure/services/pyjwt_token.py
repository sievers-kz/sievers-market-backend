import secrets
import uuid
from datetime import timedelta, datetime, timezone

import jwt

from src.api.users.user_dto import TokenDataDTO
from src.core.users.domain.enums import TokenTypeEnum


class PyJWTTokenService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_lifetime: timedelta,
        refresh_token_lifetime: timedelta,
        email_token_lifetime: timedelta
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_lifetime = access_token_lifetime
        self._refresh_token_lifetime = refresh_token_lifetime
        self._email_token_lifetime = email_token_lifetime

    def create_refresh_token(self, user_id: uuid.UUID) -> TokenDataDTO:
        expires_at = datetime.now(timezone.utc) + self._refresh_token_lifetime
        payload = {"sub": str(user_id), "exp": expires_at, "token_type": TokenTypeEnum.REFRESH_TOKEN.value}
        token_str = jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)
        return TokenDataDTO(token_str=token_str, expires_at=expires_at)

    def create_access_token(self, user_id: uuid.UUID) -> TokenDataDTO:
        expires_at = datetime.now(timezone.utc) + self._access_token_lifetime
        payload = {"sub": str(user_id), "exp": expires_at, "token_type": TokenTypeEnum.ACCESS_TOKEN.value}
        token_str = jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)
        return TokenDataDTO(token_str=token_str, expires_at=expires_at)

    def create_email_token(self, email: str) -> TokenDataDTO:
        expires_at = datetime.now(timezone.utc) + self._email_token_lifetime
        payload = {"sub": email, "exp": expires_at, "token_type": TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN.value}
        token_str = jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)
        return TokenDataDTO(token_str=token_str, expires_at=expires_at)

    def create_confirmation_code(self) -> str:
        return secrets.token_hex(3).upper()

    def verify_token(self, token: str, expected_type: TokenTypeEnum) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            token_type = payload.get("token_type")
            if not token_type or token_type != expected_type:
                raise ValueError("Wrong token type!")

        except jwt.PyJWTError as e:
            raise ValueError(f"Invalid token ...: {e}")
