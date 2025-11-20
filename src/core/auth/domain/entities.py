import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenAlreadyRevokedError, InvalidCredentialsError
from src.core.shared.domain.entities import AggregateRoot, Entity
from src.core.auth.domain.value_objects import HashedPassword


@dataclass(frozen=False)
class UserIdentity(AggregateRoot):
    id: uuid.UUID
    user_id: uuid.UUID
    credentials: "UserCredentialsIdentity"
    tokens: list["UserTokenIdentity"]

    def add_new_token(self, token_type: TokenTypeEnum, token_value: str, expires_at: datetime):
        new_token = UserTokenIdentity.create(
            auth_id=self.id,
            token_type=token_type,
            token_value=token_value,
            expires_at=expires_at
        )

        self.tokens.append(new_token)
        return new_token

    def reset_password(self, raw_password: str):
        self.credentials.change_password(raw_password)
        self.revoke_session_tokens()

    def revoke_token(self, token_value: str):
        token = self.get_token_by_value(token_value)
        if not token:
            return None
        token.revoke_token()

    def revoke_session_tokens(self):
        session_types = [TokenTypeEnum.REFRESH_TOKEN]

        for token in self.tokens:
            if token.token_type in session_types and not token.is_revoked:
                token.revoke_token()

    def get_active_token_by_value(self, token_value: str):
        for token in self.tokens:
            if token.token_value == token_value:
                if not token.is_revoked:
                    return token
        return None
    
    def get_token_by_value(self, token_value: str):
        for token in self.tokens:
            if token.token_value == token_value:
                return token
        return None

    def get_current_token(self, token_type: TokenTypeEnum):
        for token in self.tokens:
            if token.token_type == token_type:
                if not token.is_revoked:
                    return token
        return None

    def change_password(self, raw_password: str):
        self.credentials.change_password(raw_password=raw_password)


@dataclass(frozen=False)
class UserCredentialsIdentity(Entity):
    id: uuid.UUID
    auth_id: uuid.UUID
    hashed_password: HashedPassword
    password_changed_at: datetime

    def change_password(self, raw_password: str):
        self.hashed_password = HashedPassword.from_raw(raw_password)
        self.password_changed_at = datetime.utcnow()


@dataclass(frozen=False)
class UserTokenIdentity(Entity):
    id: uuid.UUID
    auth_id: uuid.UUID
    token_type: TokenTypeEnum
    token_value: str
    is_revoked: bool
    expires_at: datetime

    @classmethod
    def create(
        cls,
        auth_id: uuid.UUID,
        token_type: TokenTypeEnum,
        token_value: str,
        expires_at: datetime
    ):
        return cls(
            id=uuid.uuid4(),
            auth_id=auth_id,
            token_type=token_type,
            token_value=token_value,
            is_revoked=False,
            expires_at=expires_at
        )

    def is_expired(self):
        current_time = datetime.now(timezone.utc)
        return current_time > self.expires_at

    def revoke_token(self):
        if self.is_revoked:
            raise TokenAlreadyRevokedError(code="token_already_revoked")
        self.is_revoked = True


