from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.infrastructure.models import Color


class ColorRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Color]:
        result = await self._session.execute(select(Color))
        return result.scalars().all()

    async def get_by_id(self, color_id: UUID) -> Color | None:
        result = await self._session.execute(select(Color).where(Color.id == color_id))
        return result.scalar_one_or_none()

    async def create(self, name: str, hex: str) -> Color:
        color = Color(name=name, hex=hex)
        self._session.add(color)
        await self._session.commit()
        await self._session.refresh(color)
        return color

    async def update(
        self, color_id: UUID, name: str | None, hex: str | None
    ) -> Color | None:
        color = await self.get_by_id(color_id)
        if not color:
            return None
        if name is not None:
            color.name = name
        if hex is not None:
            color.hex = hex

        await self._session.commit()
        await self._session.refresh(color)
        return color

    async def delete(self, color_id: UUID) -> bool:
        result = await self._session.execute(delete(Color).where(Color.id == color_id))
        return result.rowcount > 0
