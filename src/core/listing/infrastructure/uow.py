from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork
from src.core.listing.infrastructure.repository import ListingRepository


class ListingUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def listing(self) -> ListingRepository:
        return ListingRepository(self._session)

