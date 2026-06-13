from typing import Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self._session: AsyncSession = None

    async def __aenter__(self):
        self._session = self._session_factory()
        try:
            await self._session.execute(text("SELECT 1"))
        except (TimeoutError, OSError) as exc:
            raise ValueError("Database connection failed") from exc
        except Exception as exc:
            raise ValueError("Unexpected error") from exc

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            if exc_type:
                await self.rollback()

            await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
