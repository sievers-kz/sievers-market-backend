from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.application.interfaces import ICategoryRepository
from src.core.catalog.domain.entities import Category as DomainCategory
from src.core.catalog.infrastructure.mappers import CategoryMapper
from src.core.catalog.infrastructure.models import Category as ORMCategory


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.category = ORMCategory

    async def get_by_id(self, category_id: UUID) -> DomainCategory:
        statement = select(self.category).where(self.category.id == category_id)
        query_result = await self._session.execute(statement)
        result = query_result.scalar_one_or_none()

        if not result:
            return None

        return CategoryMapper.to_domain(result)

    async def get_all(self) -> list[DomainCategory]:
        statement = select(self.category)
        query_result = await self._session.execute(statement)
        results = query_result.scalars().all()

        if not results:
            return None

        return [CategoryMapper.to_domain(result) for result in results]

    async def save(self, category: DomainCategory) -> None:
        mapped_model = CategoryMapper.to_orm(category)
        await self._session.merge(mapped_model)
        await self._session.flush()
