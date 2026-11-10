from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.customer.infrastructure.repository import CustomerRepository, OrganizationRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class CustomerUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def customer(self) -> CustomerRepository:
        return CustomerRepository(self._session)

    @property
    def organization(self) -> OrganizationRepository:
        return OrganizationRepository(self._session)
