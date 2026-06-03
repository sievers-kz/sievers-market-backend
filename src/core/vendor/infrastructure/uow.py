from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork
from src.core.vendor.infrastructure.repository import VendorRepository


class VendorUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def vendor(self) -> VendorRepository:
        return VendorRepository(self._session)
