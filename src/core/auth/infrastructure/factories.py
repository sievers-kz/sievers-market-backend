import uuid
from datetime import datetime

from src.api.auth.auth_dto import UserCredentialsDTO, AuthTokenDTO

from src.core.auth.domain.entities import (
    UserIdentity as DomainUserIdentity,
    UserCredentialsIdentity as DomainUserCredentialsIdentity,
    UserTokenIdentity as DomainUserTokenIdentity
)

from src.core.users.domain.value_objects import HashedPassword


class UserIdentityFactory:
    @staticmethod
    def create(
        user_id: uuid.UUID,
        credentials: UserCredentialsDTO,
        tokens: AuthTokenDTO
    ) -> DomainUserIdentity:

        auth_id = uuid.uuid4()
        credentials = _UserCredentialsIdentityFactory.create(credentials, auth_id)
        tokens = _UserTokenIdentityFactory.create(tokens, auth_id)

        return DomainUserIdentity(
            id=auth_id,
            user_id=user_id,
            credentials=credentials,
            tokens=tokens
        )


class _UserCredentialsIdentityFactory:
    @staticmethod
    def create(dto: UserCredentialsDTO, auth_id: uuid.UUID) -> DomainUserCredentialsIdentity:
        return DomainUserCredentialsIdentity(
            id=uuid.uuid4(),
            auth_id=auth_id,
            hashed_password=HashedPassword.from_raw(dto.raw_password),
            password_changed_at=datetime.utcnow()
        )


class _UserTokenIdentityFactory:
    @staticmethod
    def create(tokens_dto: list[AuthTokenDTO], auth_id: uuid.UUID) -> DomainUserTokenIdentity:
        return [
            DomainUserTokenIdentity(
                id=uuid.uuid4(),
                auth_id=auth_id,
                token_type=dto.token_type,
                token_value=dto.token_value,
                is_revoked=False,
                expires_at=dto.expires_at
            ) for dto in tokens_dto
        ]