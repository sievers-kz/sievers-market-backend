from src.configuration.database.models.users import AuthToken
from src.core.auth.domain.entities import AuthTokenAggregate


class AuthTokenMapper:
    @staticmethod
    def to_orm(token_aggregate: AuthTokenAggregate) -> AuthToken:
        return AuthToken(
            id=token_aggregate.id,
            user_id=token_aggregate.user_id,
            token_type=token_aggregate.token_type,
            token_value=token_aggregate.token_value,
            is_revoked=token_aggregate.is_revoked,
            expires_at=token_aggregate.expires_at
        )

    @staticmethod
    def to_domain(token_model: AuthToken) -> AuthTokenAggregate:
        return AuthTokenAggregate(
            id=token_model.id,
            user_id=token_model.user_id,
            token_type=token_model.token_type,
            token_value=token_model.token_value,
            is_revoked=token_model.is_revoked,
            expires_at=token_model.expires_at
        )
