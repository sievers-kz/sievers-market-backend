from sqlalchemy.ext.asyncio import AsyncSession

from src.core.iam.infrastructure.repository import AccountRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class IAMUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def account(self):
        if self._session is None:
            raise RuntimeError("UoW not initialized!")
        return AccountRepository(self._session)

