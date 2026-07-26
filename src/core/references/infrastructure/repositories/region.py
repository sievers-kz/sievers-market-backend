from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.references.infrastructure.models import Region


class RegionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Region]:
        result = await self._session.execute(
            select(Region).options(selectinload(Region.cities))
        )
        return result.scalars().all()

    async def get_by_id(self, region_id: UUID) -> Region | None:
        result = await self._session.execute(
            select(Region)
            .options(selectinload(Region.cities))
            .where(Region.id == region_id)
        )
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Region:
        region = Region(name=name)
        self._session.add(region)
        await self._session.commit()
        await self._session.refresh(region)
        return region

    async def update(self, region_id: UUID, name: str) -> Region | None:
        region = await self.get_by_id(region_id)
        if not region:
            return None
        region.name = name

        await self._session.commit()
        await self._session.refresh(region)
        return region

    async def delete(self, region_id: UUID) -> bool:
        result = await self._session.execute(
            delete(Region).where(Region.id == region_id)
        )
        return result.rowcount > 0
