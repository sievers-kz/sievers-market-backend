from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.machinery.application.interfaces.repository import IMachineryRepository
from src.core.machinery.infrastructure.mapper import MachineryMapper
from src.core.machinery.infrastructure.models import Machinery as ORMMachinery
from src.core.machinery.domain.entities import Machinery as DomainMachinery
from src.core.shared.domain.enums import ListingStatus


class MachineryRepository(IMachineryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._machinery = ORMMachinery

    async def save(self, machinery: DomainMachinery) -> None:
        mapped_model = MachineryMapper.to_orm(machinery)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_machinery_by_id(self, machinery_id: UUID) -> DomainMachinery:
        statement = select(self._machinery).where(self._machinery.id == machinery_id)
        query_result = await self._session.execute(statement)
        result = query_result.scalar_one_or_none()

        if result is None:
            return None

        return MachineryMapper.to_domain(result)

    async def count_customer_machinery(self, customer_id: UUID) -> int:
        statement = (
            select(func.count())
            .select_from(self._machinery)
            .where(
                self._machinery.customer_id == customer_id,
                self._machinery.status == ListingStatus.ACTIVE
            )
        )

        return await self._session.scalar(statement)
