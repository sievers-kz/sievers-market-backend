from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.users.application.uow import AbstractUserUnitOfWork
from src.core.users.infrastructure.user_repository import UserRepository, AuthTokenRepository


class UserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory)

    @property
    def user(self):
        if self.session is None:
            raise RuntimeError("UoW not initialized!")
        return UserRepository(self.session)

    @property
    def token(self):
        if self.session is None:
            raise RuntimeError("UoW not initialized!")
        return AuthTokenRepository(self.session)

    async def commit(self):
        if self.session is None:
            raise RuntimeError("No active session!")
        await self.session.commit()

    async def rollback(self):
        if self.session is None:
            raise RuntimeError("No active session!")
        await self.session.rollback()

