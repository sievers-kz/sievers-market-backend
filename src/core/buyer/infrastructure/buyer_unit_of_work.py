from sqlalchemy.ext.asyncio import AsyncSession

from src.core.buyer.infrastructure.repository import BuyerRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class BuyerUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def buyer(self):
        return BuyerRepository(self._session)
