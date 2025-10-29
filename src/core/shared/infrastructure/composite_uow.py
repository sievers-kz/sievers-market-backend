from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.infrastructure.auth_repository import UserIdentityRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork
from src.core.users.infrastructure.user_repository import UserRepository


class UserIdentityUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def user(self):
        return UserRepository(self._session)

    @property
    def identity(self):
        return UserIdentityRepository(self._session)
