from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.customer.domain.entities import Customer as DomainCustomer
from src.core.customer.domain.entities import Organization as DomainOrganization
from src.core.customer.infrastructure.mapper import CustomerMapper, OrganizationMapper
from src.core.customer.infrastructure.models import Customer as ORMCustomer
from src.core.customer.infrastructure.models import Organization as ORMOrganization


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._model = ORMCustomer

    async def save(self, customer: DomainCustomer) -> None:
        mapped_model = CustomerMapper.to_orm(customer)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_by_id(self, customer_id: UUID) -> DomainCustomer:
        statement = select(self._model).where(self._model.id == customer_id)

        result = (await self._session.execute(statement)).scalar_one_or_none()
        if result is None:
            return None
        return CustomerMapper.to_domain(result)

    async def get_by_account_id(self, account_id: UUID) -> DomainCustomer:
        statement = select(self._model).where(self._model.account_id == account_id)

        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None

        return CustomerMapper.to_domain(orm_model)


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._model = ORMOrganization

    async def save(self, organization: DomainOrganization) -> None:
        mapped_model = OrganizationMapper.to_orm(organization)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_by_id(self, organization_id: UUID) -> DomainOrganization:
        statement = select(self._model).where(self._model.id == organization_id)
        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None
        return OrganizationMapper.to_domain(orm_model)

    async def get_by_owner_id(self, owner_id: UUID) -> DomainOrganization:
        statement = select(self._model).where(self._model.owner_id == owner_id)
        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None
        return OrganizationMapper.to_domain(orm_model)
