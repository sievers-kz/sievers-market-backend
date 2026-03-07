from sqlalchemy.ext.asyncio import AsyncSession

from src.core.customer.infrastructure.repository import CustomerRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class CustomerUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def customer(self):
        return CustomerRepository(self._session)
