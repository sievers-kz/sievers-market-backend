from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.infrastructure.auth_repository import AuthTokenRepository
from src.core.users.infrastructure.user_unit_of_work import SQLAlchemyUnitOfWork


class AuthUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def token(self):
        if self._session is None:
            raise RuntimeError("UoW not initialized!")
        return AuthTokenRepository(self._session)
