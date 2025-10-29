import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.auth.infrastructure.mappers import UserIdentityMapper

from src.core.auth.infrastructure.models import (
    UserIdentity as UserIdentityModel,
    UserCredentialsIdentity as UserCredentialsIdentityModel,
    UserTokenIdentity as UserTokenIdentityModel
)

from src.core.auth.domain.entities import UserIdentity as DomainUserIdentity


class UserIdentityRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._auth_model = UserIdentityModel
        self._credential_model = UserCredentialsIdentityModel
        self._token_model = UserTokenIdentityModel

    async def get_user_identity(self, user_id: uuid.UUID) -> DomainUserIdentity:
        statement = (
            select(self._auth_model)
            .options(
                joinedload(self._auth_model.credentials),
                joinedload(self._auth_model.tokens)
            ).where(self._auth_model.user_id == user_id)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.unique().scalar_one_or_none()

        if orm_model is None:
            return None

        return UserIdentityMapper.to_domain(orm_model)

    async def find_by_token_value(self, token_value: str) -> DomainUserIdentity:
        statement = (
            select(self._auth_model)
            .join(self._token_model)
            .where(self._token_model.token_value == token_value)
            .options(
                joinedload(self._auth_model.credentials),
                joinedload(self._auth_model.tokens)
            )
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.unique().scalar_one_or_none()

        if orm_model is None:
            return None

        return UserIdentityMapper.to_domain(orm_model)

    async def save(self, user_auth: DomainUserIdentity) -> None:
        orm_model = UserIdentityMapper.to_orm(user_auth)
        await self._session.merge(orm_model)
        await self._session.flush()
