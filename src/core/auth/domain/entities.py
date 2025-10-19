import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenAlreadyRevokedError


@dataclass
class AuthTokenAggregate:
    id: uuid.UUID
    user_id: uuid.UUID
    token_type: TokenTypeEnum
    token_value: str
    is_revoked: bool
    expires_at: datetime

    def is_expired(self):
        current_time = datetime.now(timezone.utc)
        return current_time > self.expires_at

    def revoke_token(self):
        if self.is_revoked:
            raise TokenAlreadyRevokedError(code="token_already_revoked")
        self.is_revoked = True
