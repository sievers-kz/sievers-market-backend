from src.core.auth.domain.entities import (
    UserIdentity as DomainUserIdentity,
    UserCredentialsIdentity as DomainUserCredentialIdentity,
    UserTokenIdentity as DomainUserTokenIdentity
)

from src.core.auth.infrastructure.models import (
    UserIdentity as UserIdentityModel,
    UserCredentialsIdentity as UserCredentialsIdentityModel,
    UserTokenIdentity as UserTokenIdentityModel
)
from src.core.users.domain.value_objects import HashedPassword


class UserIdentityMapper:
    @staticmethod
    def to_domain(orm_model: UserIdentityModel) -> DomainUserIdentity:
        _credentials = _UserCredentialsIdentityMapper.to_domain(orm_model.credentials)
        _tokens = [_UserTokenIdentityMapper.to_domain(token) for token in orm_model.tokens]

        return DomainUserIdentity(
            id=orm_model.id,
            user_id=orm_model.user_id,
            credentials=_credentials,
            tokens=_tokens
        )

    @staticmethod
    def to_orm(domain_model: DomainUserIdentity) -> UserIdentityModel:
        _credentials = _UserCredentialsIdentityMapper.to_orm(domain_model.credentials)
        _tokens = [_UserTokenIdentityMapper.to_orm(token) for token in domain_model.tokens]

        return UserIdentityModel(
            id=domain_model.id,
            user_id=domain_model.user_id,
            credentials=_credentials,
            tokens=_tokens
        )


class _UserCredentialsIdentityMapper:
    @staticmethod
    def to_domain(orm_model: UserCredentialsIdentityModel) -> DomainUserCredentialIdentity:
        return DomainUserCredentialIdentity(
            id=orm_model.id,
            auth_id=orm_model.auth_id,
            hashed_password=HashedPassword.from_hash(orm_model.hashed_password),
            password_changed_at=orm_model.password_changed_at
        )

    @staticmethod
    def to_orm(domain_model: DomainUserCredentialIdentity) -> UserCredentialsIdentityModel:
        return UserCredentialsIdentityModel(
            id=domain_model.id,
            auth_id=domain_model.auth_id,
            hashed_password=domain_model.hashed_password.hashed_password,
            password_changed_at=domain_model.password_changed_at
        )


class _UserTokenIdentityMapper:
    @staticmethod
    def to_domain(orm_model: UserTokenIdentityModel) -> DomainUserTokenIdentity:
        return DomainUserTokenIdentity(
            id=orm_model.id,
            auth_id=orm_model.auth_id,
            token_type=orm_model.token_type,
            token_value=orm_model.token_value,
            is_revoked=orm_model.is_revoked,
            expires_at=orm_model.expires_at
        )

    @staticmethod
    def to_orm(domain_model: DomainUserTokenIdentity) -> UserTokenIdentityModel:
        return UserTokenIdentityModel(
            id=domain_model.id,
            auth_id=domain_model.auth_id,
            token_type=domain_model.token_type,
            token_value=domain_model.token_value,
            is_revoked=domain_model.is_revoked,
            expires_at=domain_model.expires_at
        )
