from typing import Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.listings.infrastructure.query_services.filter_query import FilterQueryService
from src.core.listings.infrastructure.query_services.listing_query import ListingQueryService


class ListingQueryContext:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self._session = None

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
    def listing(self):
        return ListingQueryService(self._session)

    @property
    def filter(self):
        return FilterQueryService(self._session)
