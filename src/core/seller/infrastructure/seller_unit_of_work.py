from sqlalchemy.ext.asyncio import AsyncSession

from src.core.seller.infrastructure.repository import SellerRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class SellerUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def seller(self):
        return SellerRepository(self._session)
