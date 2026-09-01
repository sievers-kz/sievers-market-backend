from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.infrastructure.enums import CatalogStatus
from src.core.catalog.infrastructure.models import Category, Rubric, Subcategory


class RubricRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, rubric_id: UUID) -> Rubric | None:
        return await self._session.get(Rubric, rubric_id)

    async def get_all(self) -> list[Rubric]:
        result = await self._session.execute(select(Rubric))
        return list(result.scalars().all())

    async def create(self, name: str) -> Rubric:
        rubric = Rubric(name=name, status=CatalogStatus.ACTIVE)
        self._session.add(rubric)
        await self._session.commit()
        await self._session.refresh(rubric)
        return rubric

    async def save(self, rubric: Rubric) -> None:
        self._session.add(rubric)
        await self._session.commit()


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, category_id: UUID) -> Category | None:
        return await self._session.get(Category, category_id)

    async def get_all(self) -> list[Category]:
        result = await self._session.execute(select(Category))
        return list(result.scalars().all())

    async def create(self, rubric_id: UUID, name: str) -> Category:
        category = Category(rubric_id=rubric_id, name=name, status=CatalogStatus.ACTIVE)
        self._session.add(category)
        await self._session.commit()
        await self._session.refresh(category)
        return category

    async def save(self, category: Category) -> None:
        self._session.add(category)
        await self._session.commit()


class SubcategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, subcategory_id: UUID) -> Subcategory | None:
        return await self._session.get(Subcategory, subcategory_id)

    async def get_all(self) -> list[Subcategory]:
        result = await self._session.execute(select(Subcategory))
        return list(result.scalars().all())

    async def create(self, category_id: UUID, name: str) -> Subcategory:
        subcategory = Subcategory(
            category_id=category_id, name=name, status=CatalogStatus.ACTIVE
        )
        self._session.add(subcategory)
        await self._session.commit()
        await self._session.refresh(subcategory)
        return subcategory

    async def save(self, subcategory: Subcategory) -> None:
        self._session.add(subcategory)
        await self._session.commit()
