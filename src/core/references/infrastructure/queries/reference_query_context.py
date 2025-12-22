from typing import Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.infrastructure.queries.reference import ReferenceQueryService, CategoryQueryService, \
    SpecificationQueryService


class ReferenceQueryContext:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self._session: AsyncSession = None

    async def __aenter__(self):
        try:
            self._session = self._session_factory()
            await self._session.execute(text("SELECT 1"))
            return self
        except Exception as e:
            raise e

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    @property
    def reference(self):
        return ReferenceQueryService(self._session)

    @property
    def category(self):
        return CategoryQueryService(self._session)

    @property
    def specification(self):
        return SpecificationQueryService(self._session)
