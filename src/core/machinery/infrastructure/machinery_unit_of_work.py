from sqlalchemy.ext.asyncio import AsyncSession

from src.core.machinery.infrastructure.repository import MachineryRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class MachineryUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def machinery(self):
        return MachineryRepository(self._session)
