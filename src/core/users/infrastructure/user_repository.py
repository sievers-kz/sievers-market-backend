import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.users.domain.entities import UserAggregate, AuthTokenAggregate
from src.core.users.domain.interfaces import AbstractRepository
from src.core.users.infrastructure.mappers import UserMapper, AuthTokenMapper
from src.configuration.database.models.users import User, AuthToken


class UserRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> "":
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def save(self, user: UserAggregate) -> None:
        user_orm = UserMapper.to_orm(user)
        self.session.add(user_orm)
        await self.session.commit()

    async def get_by_email(self, email: str) -> UserAggregate:
        statement = (
            select(User)
            .options(
                joinedload(User.individual_profile),
                joinedload(User.business_profile),
                joinedload(User.auth)
            ).where(User.email == email)
        )

        result = await self.session.execute(statement)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return UserMapper.to_domain(user_model)


class AuthTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_value(self, token_value: str) -> AuthTokenAggregate:
        statement = select(AuthToken).where(AuthToken.token_value == token_value)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalar_one_or_none())

    async def find_by_user_id(self, user_id: uuid.UUID) -> list[AuthTokenAggregate]:
        statement = select(AuthToken).where(AuthToken.user_id == user_id)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalars().all())

    async def find_by_token_id(self, token_id: uuid.UUID) -> AuthTokenAggregate:
        statement = select(AuthToken).where(AuthToken.id == token_id)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalar_one_or_none())

    async def save(self, token_aggregate: AuthTokenAggregate) -> None:
        token_model = AuthTokenMapper.to_orm(token_aggregate)
        self._session.add(token_model)
        await self._session.commit()
