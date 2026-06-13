from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.listing.infrastructure.repository import ListingRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class ListingUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def listing(self) -> ListingRepository:
        return ListingRepository(self._session)
