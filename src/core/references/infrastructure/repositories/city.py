from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.references.infrastructure.models import City


class CityRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[City]:
        result = await self._session.execute(
            select(City).options(selectinload(City.region))
        )
        return result.scalars().all()

    async def get_by_id(self, city_id: UUID) -> City | None:
        result = await self._session.execute(
            select(City).options(selectinload(City.region)).where(City.id == city_id)
        )
        return result.scalar_one_or_none()

    async def get_by_region(self, region_id: UUID) -> list[City]:
        result = await self._session.execute(
            select(City)
            .options(selectinload(City.region))
            .where(City.region_id == region_id)
        )
        return result.scalars().all()

    async def create(self, name: str, region_id: UUID) -> City:
        city = City(name=name, region_id=region_id)
        self._session.add(city)
        await self._session.commit()
        await self._session.refresh(city)
        return city

    async def update(
        self, city_id: UUID, name: str | None, region_id: UUID | None
    ) -> City | None:
        city = await self.get_by_id(city_id)
        if not city:
            return None
        if name is not None:
            city.name = name
        if region_id is not None:
            city.region_id = region_id

        await self._session.commit()
        await self._session.refresh(city)
        return city

    async def delete(self, city_id: UUID) -> bool:
        result = await self._session.execute(delete(City).where(City.id == city_id))
        return result.rowcount > 0
