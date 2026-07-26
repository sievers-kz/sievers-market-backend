from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.infrastructure.models import Brand


class BrandRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Brand]:
        result = await self._session.execute(select(Brand))
        return result.scalars().all()

    async def get_by_id(self, brand_id: UUID) -> Brand | None:
        result = await self._session.execute(select(Brand).where(Brand.id == brand_id))
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Brand:
        brand = Brand(name=name)
        self._session.add(brand)
        await self._session.commit()
        await self._session.refresh(brand)
        return brand

    async def update(self, brand_id: UUID, name: str) -> Brand | None:
        brand = await self.get_by_id(brand_id)
        if not brand:
            return None

        brand.name = name
        await self._session.commit()
        await self._session.refresh(brand)
        return brand

    async def delete(self, brand_id: UUID) -> bool:
        result = await self._session.execute(delete(Brand).where(Brand.id == brand_id))
        return result.rowcount > 0
