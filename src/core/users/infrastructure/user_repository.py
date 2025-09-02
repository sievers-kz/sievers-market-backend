import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.users.domain.entities import UserAggregate
from src.core.users.domain.interfaces import AbstractRepository
from src.core.users.infrastructure.mappers import UserORMMapper
from src.configuration.database.models.users import User


class UserRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> "":
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def save(self, user: UserAggregate) -> None:
        user_orm = UserORMMapper.to_orm(user)
        self.session.add(user_orm)
        await self.session.commit()

    async def get_by_email(self, email: str) -> "":
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
