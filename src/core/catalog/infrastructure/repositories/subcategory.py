from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.application.interfaces import ISubcategoryRepository
from src.core.catalog.domain.entities import Subcategory as DomainSubcategory
from src.core.catalog.infrastructure.mappers import SubcategoryMapper
from src.core.catalog.infrastructure.models import Subcategory as ORMSubcategory


class SubcategoryRepository(ISubcategoryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.subcategory = ORMSubcategory

    async def get_by_id(self, subcategory_id: UUID) -> DomainSubcategory:
        statement = select(self.subcategory).where(
            self.subcategory.id == subcategory_id
        )
        query_result = await self._session.execute(statement)
        result = query_result.scalar_one_or_none()

        if not result:
            return None

        return SubcategoryMapper.to_domain(result)

    async def get_all(self) -> list[DomainSubcategory]:
        statement = select(self.subcategory)
        query_result = await self._session.execute(statement)
        results = query_result.scalars().all()

        if not results:
            return None

        return [SubcategoryMapper.to_domain(result) for result in results]

    async def save(self, subcategory: DomainSubcategory) -> None:
        mapped_model = SubcategoryMapper.to_orm(subcategory)
        await self._session.merge(mapped_model)
        await self._session.flush()
