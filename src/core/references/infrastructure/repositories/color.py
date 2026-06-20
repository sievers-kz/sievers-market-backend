from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.application.interfaces.abstract_color_repository import (
    IColorRepository,
)
from src.core.references.domain.entities import Color as DomainColor
from src.core.references.infrastructure.models import Color as ORMColor


class ColorRepository(IColorRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.color = ORMColor

    async def get_all(self) -> list[DomainColor]:
        statement = select(self.color)
        query_result = await self._session.execute(statement)
        results = query_result.scalars().all()

        if results is None:
            return []

        return [
            DomainColor(
                id=color.id, name=color.name, hex=color.hex, status=color.status
            )
            for color in results
        ]

    async def get_by_id(self, color_id: UUID) -> DomainColor:
        statement = select(self.color).where(self.color.id == color_id)
        query_result = await self._session.execute(statement)
        result = query_result.scalars().first()

        if result is None:
            return None

        return DomainColor(
            id=result.id, name=result.name, hex=result.hex, status=result.status
        )

    async def save(self, color: DomainColor) -> None:
        mapped = ORMColor(
            id=color.id, name=color.name, hex=color.hex, status=color.status
        )
        await self._session.merge(mapped)
        await self._session.commit()
