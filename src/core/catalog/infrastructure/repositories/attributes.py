from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.catalog.infrastructure.models import (
    AttributeDefinition,
    AttributeGroup,
    SubcategoryAttribute,
    UnitOfMeasure,
)


class AttributeDefinitionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> AttributeDefinition | None:
        return await self._session.get(AttributeDefinition, id)

    async def get_all(self) -> list[AttributeDefinition]:
        result = await self._session.execute(select(AttributeDefinition))
        return list(result.scalars().all())

    async def create(
        self, key: str, label: str, type, options: list, source: str
    ) -> AttributeDefinition:
        definition = AttributeDefinition(
            key=key, label=label, type=type, options=options, source=source
        )
        self._session.add(definition)
        await self._session.commit()
        await self._session.refresh(definition)
        return definition

    async def save(self, definition: AttributeDefinition) -> None:
        self._session.add(definition)
        await self._session.commit()


class AttributeGroupRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> AttributeGroup | None:
        return await self._session.get(AttributeGroup, id)

    async def get_all(self) -> list[AttributeGroup]:
        result = await self._session.execute(select(AttributeGroup))
        return list(result.scalars().all())

    async def create(self, key: str, label: str, position: int) -> AttributeGroup:
        group = AttributeGroup(key=key, label=label, position=position)
        self._session.add(group)
        await self._session.commit()
        await self._session.refresh(group)
        return group


class UnitOfMeasureRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> UnitOfMeasure | None:
        return await self._session.get(UnitOfMeasure, id)

    async def get_all(self) -> list[UnitOfMeasure]:
        result = await self._session.execute(select(UnitOfMeasure))
        return list(result.scalars().all())

    async def create(self, key: str, label: str) -> UnitOfMeasure:
        unit = UnitOfMeasure(key=key, label=label)
        self._session.add(unit)
        await self._session.commit()
        await self._session.refresh(unit)
        return unit


class SubcategoryAttributeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UUID) -> SubcategoryAttribute | None:
        return await self._session.get(SubcategoryAttribute, id)

    async def get_with_definitions(
        self, subcategory_id: UUID
    ) -> list[SubcategoryAttribute]:
        statement = (
            select(SubcategoryAttribute)
            .where(SubcategoryAttribute.subcategory_id == subcategory_id)
            .options(
                joinedload(SubcategoryAttribute.attribute),
                joinedload(SubcategoryAttribute.group),
                joinedload(SubcategoryAttribute.unit),
            )
            .order_by(SubcategoryAttribute.position)
        )
        result = await self._session.execute(statement)
        return list(result.scalars().unique().all())

    async def create(
        self,
        subcategory_id: UUID,
        attribute_id: UUID,
        group_id: UUID,
        unit_id: UUID | None,
        required: bool,
        filterable: bool,
        position: int,
    ) -> SubcategoryAttribute:
        link = SubcategoryAttribute(
            subcategory_id=subcategory_id,
            attribute_id=attribute_id,
            group_id=group_id,
            unit_id=unit_id,
            required=required,
            filterable=filterable,
            position=position,
        )
        self._session.add(link)
        await self._session.commit()
        await self._session.refresh(link)
        return link

    async def delete(self, id: UUID) -> None:
        link = await self._session.get(SubcategoryAttribute, id)
        if link:
            await self._session.delete(link)
