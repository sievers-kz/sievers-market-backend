from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.application.interfaces import IRubricRepository
from src.core.catalog.infrastructure.mappers import RubricMapper

from src.core.catalog.infrastructure.models import (
    Rubric as ORMRubric,
)

from src.core.catalog.domain.entities import (
    Rubric as DomainRubric,
)


class RubricRepository(IRubricRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.rubric = ORMRubric

    async def get_by_id(self, rubric_id: UUID) -> DomainRubric:
        statement = select(self.rubric).where(self.rubric.id == rubric_id)
        query_result = await self._session.execute(statement)
        result = query_result.scalar_one_or_none()

        if not result:
            return None

        return RubricMapper.to_domain(result)

    async def get_all(self) -> list[DomainRubric]:
        statement = select(self.rubric)
        query_result = await self._session.execute(statement)
        results = query_result.scalars().all()

        if not results:
            return None

        return [RubricMapper.to_domain(result) for result in results]

    async def save(self, rubric: DomainRubric) -> None:
        mapped_model = RubricMapper.to_orm(rubric)
        await self._session.merge(mapped_model)
        await self._session.flush()