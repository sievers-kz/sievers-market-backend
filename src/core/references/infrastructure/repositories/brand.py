from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.application.interfaces.abstract_brand_repository import IBrandRepository
from src.core.references.infrastructure.models import Brand as ORMBrand
from src.core.references.domain.entities import Brand as DomainBrand


class BrandRepository(IBrandRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.brand = ORMBrand

    async def get_all(self):
        statement = select(self.brand)
        query_result = await self._session.execute(statement)
        results = query_result.scalars().all()
        return [DomainBrand(id=brand.id, name=brand.name) for brand in results]

    async def get_by_id(self, brand_id: UUID):
        statement = select(self.brand).where(self.brand.id == brand_id)
        query_result = await self._session.execute(statement)
        result = query_result.scalars().first()
        return DomainBrand(id=result.id, name=result.name)

    async def save(self, brand: DomainBrand) -> None:
        mapped = self.brand(id=brand.id, name=brand.name)
        await self._session.merge(mapped)
        await self._session.commit()

    async def delete(self, brand_id: UUID) -> None:
        statement = delete(self.brand).where(self.brand.id == brand_id)
        await self._session.execute(statement)
