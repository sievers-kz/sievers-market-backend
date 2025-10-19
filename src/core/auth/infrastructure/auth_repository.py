import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configuration.database.models.users import AuthToken
from src.core.auth.domain.entities import AuthTokenAggregate
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.mappers import AuthTokenMapper


class AuthTokenRepository: # FIXME: Set a simple validation if result return None
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_value(self, token_value: str) -> AuthTokenAggregate:
        statement = select(AuthToken).where(AuthToken.token_value == token_value)
        query_result = await self._session.execute(statement)
        token_model = query_result.scalar_one_or_none()

        if token_model is None:
            return None

        return AuthTokenMapper.to_domain(token_model)

    async def find_by_user_id(self, user_id: uuid.UUID) -> list[AuthTokenAggregate]:
        statement = select(AuthToken).where(AuthToken.user_id == user_id)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalars().all())

    async def find_by_token_id(self, token_id: uuid.UUID) -> AuthTokenAggregate:
        statement = select(AuthToken).where(AuthToken.id == token_id)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalar_one_or_none())

    async def find_all_refresh_tokens_by_user_id(self, user_id: uuid.UUID) -> list[AuthTokenAggregate]:
        statement = (
            select(AuthToken)
            .where(
                AuthToken.user_id == user_id,
                AuthToken.token_type == TokenTypeEnum.REFRESH_TOKEN,
                AuthToken.is_revoked == False
            )
        )

        query_result = await self._session.execute(statement)
        orm_tokens = query_result.scalars().all()
        return [AuthTokenMapper.to_domain(token) for token in orm_tokens]

    async def save(self, token_aggregate: AuthTokenAggregate) -> None:
        token_model = AuthTokenMapper.to_orm(token_aggregate)
        await self._session.merge(token_model)
        await self._session.flush()
