from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork
from src.core.users.infrastructure.user_repository import UserRepository


class UserUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def user(self):
        if self._session is None:
            raise RuntimeError("UoW not initialized!")
        return UserRepository(self._session)



