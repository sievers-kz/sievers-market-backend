from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.application.interfaces.abstract_uow import AbstractUnitOfWork


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _connect(self):
        try:
            await self._session.execute(text("SELECT 1"))
        except (TimeoutError, OSError) as exc:
            raise ValueError("Database connection failed") from exc

        except Exception as exc:
            raise ValueError("Unexpected error") from exc

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
