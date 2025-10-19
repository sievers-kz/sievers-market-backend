from typing import Callable, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.application.abstract_uow import AbstractUnitOfWork
from src.core.shared.infrastructure.exceptions.exception_classes import DatabaseConnectionError, UnitOfWorkError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession],):
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None

    async def _connect(self):
        try:
            self._session = self._session_factory()
            await self._session.execute(text("SELECT 1"))

        except (TimeoutError, OSError) as exc:
            raise DatabaseConnectionError(
                code="database_connection_error",
                details=str(exc),
                context={"operation": "connect"}
            ) from exc

        except Exception as exc:
            raise UnitOfWorkError(
                code="unexpected_error",
                details=str(exc),
                context={"operation": "connect"}
            ) from exc

    async def _close(self):
        await self._session.close()
        self._session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()