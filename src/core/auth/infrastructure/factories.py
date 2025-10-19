import uuid
from datetime import datetime

from src.core.auth.domain.entities import AuthTokenAggregate
from src.core.auth.domain.enums import TokenTypeEnum


class AuthTokenFactory:
    @staticmethod
    def create_refresh_token(
        user_id: uuid.UUID,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenFactory._create(
            user_id=user_id,
            token_type=TokenTypeEnum.REFRESH_TOKEN,
            token_value=token_value,
            expires_at=expires_at
        )

    @staticmethod
    def create_email_token(
        user_id: uuid.UUID,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenFactory._create(
            user_id=user_id,
            token_type=TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN,
            token_value=token_value,
            expires_at=expires_at
        )

    @staticmethod
    def create_password_reset_token(
        user_id: uuid.UUID,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenFactory._create(
            user_id=user_id,
            token_type=TokenTypeEnum.PASSWORD_RESET_TOKEN,
            token_value=token_value,
            expires_at=expires_at
        )

    @staticmethod
    def _create(
        user_id: uuid.UUID,
        token_type: TokenTypeEnum,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenAggregate(
            id=uuid.uuid4(),
            user_id=user_id,
            token_type=token_type,
            token_value=token_value,
            is_revoked=False,
            expires_at=expires_at
        )