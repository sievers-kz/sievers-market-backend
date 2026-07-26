from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.infrastructure.models import Country


class CountryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Country]:
        result = await self._session.execute(select(Country))
        return result.scalars().all()

    async def get_by_id(self, country_id: UUID) -> Country | None:
        result = await self._session.execute(
            select(Country).where(Country.id == country_id)
        )
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Country:
        country = Country(name=name)
        self._session.add(country)
        await self._session.commit()
        await self._session.refresh(country)
        return country

    async def update(self, country_id: UUID, name: str) -> Country | None:
        country = await self.get_by_id(country_id)
        if not country:
            return None
        country.name = name

        await self._session.commit()
        await self._session.refresh(country)
        return country

    async def delete(self, country_id: UUID) -> bool:
        result = await self._session.execute(
            delete(Country).where(Country.id == country_id)
        )
        return result.rowcount > 0
