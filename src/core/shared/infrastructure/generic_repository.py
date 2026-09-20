from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.infrastructure.base_model import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class GenericRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession):
        self.model = model
        self._session = session

    async def get_all(self) -> list[ModelT]:
        result = await self._session.execute(select(self.model))
        return list(result.scalars().all())

    async def get_by_id(self, entity_id: UUID) -> ModelT | None:
        result = await self._session.execute(select(self.model).where(self.model.id == entity_id))
        return result.scalar_one_or_none()

    async def create(self, **fields) -> ModelT:
        entity = self.model(**fields)
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def update(self, entity_id: UUID, **fields) -> ModelT | None:
        entity = await self.get_by_id(entity_id)
        if entity is None:
            return None

        for field, value in fields.items():
            if value is not None:
                setattr(entity, field, value)

        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity_id: UUID) -> bool:
        result = await self._session.execute(delete(self.model).where(self.model.id == entity_id))
        return result.rowcount > 0
