from typing import Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.users.application.uow import AbstractUserUnitOfWork, AbstractUnitOfWork
from src.core.users.infrastructure.user_repository import UserRepository, AuthTokenRepository


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self._session = None

    async def _connect(self):
        self._session = self._session_factory()
        await self._session.execute(text("SELECT 1"))

    async def _close(self):
        await self._session.close()
        self._session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class UserUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory)

    @property
    def user(self):
        if self._session is None:
            raise RuntimeError("UoW not initialized!")
        return UserRepository(self._session)

    @property
    def token(self):
        if self._session is None:
            raise RuntimeError("UoW not initialized!")
        return AuthTokenRepository(self._session)

