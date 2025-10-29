import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.users.infrastructure.mappers import UserMapper

from src.core.users.infrastructure.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    BusinessDetails as BusinessDetailsModel
)

from src.core.users.domain.entities import User as DomainUser


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._user_model = UserModel
        self._profile_model = UserProfileModel
        self._business_details_model = BusinessDetailsModel

    async def get_user_by_id(self, user_id: uuid.UUID) -> DomainUser:
        statement = (
            select(self._user_model)
            .options(
                joinedload(self._user_model.profile),
                joinedload(self._user_model.business_details)
            ).where(self._user_model.id == user_id)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None

        return UserMapper.to_domain(orm_model)

    async def get_by_user_email(self, email: str) -> DomainUser:
        statement = (
            select(self._user_model)
            .options(
                joinedload(self._user_model.profile),
                joinedload(self._user_model.business_details)
            ).where(self._user_model.email == email)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None

        return UserMapper.to_domain(orm_model)

    async def save(self, user: DomainUser) -> None:
        orm_model = UserMapper.to_orm(user)
        await self._session.merge(orm_model)
        await self._session.flush()
