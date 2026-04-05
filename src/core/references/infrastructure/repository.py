from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core.references.application.interfaces.abstract_attribute_repository import AbstractAttributeRepository
from src.core.references.application.interfaces.abstract_brand_repository import AbstractBrandRepository
from src.core.references.application.interfaces.abstract_color_repository import AbstractColorRepository
from src.core.references.application.interfaces.abstract_country_repository import AbstractCountryRepository
from src.core.references.application.interfaces.abstract_region_repository import AbstractRegionRepository
from src.core.references.application.interfaces.abstract_subcategory_repository import AbstractSubcategoryRepository

from src.core.references.infrastructure.models import (
    Attribute,
    SubcategoryAttribute,
    Subcategory,
    Category,
    Region,
    Brand,
    Country,
    Color
)


class AttributeRepository(AbstractAttributeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.attribute = Attribute
        self.subcategory_attribute = SubcategoryAttribute

    async def get_by_subcategory_id(self, subcategory_id: UUID):
        statement = (
            select(self.subcategory_attribute)
            .options(
                joinedload(self.subcategory_attribute.subcategory),
                joinedload(self.subcategory_attribute.attribute)
                .selectinload(self.attribute.options),
                joinedload(self.subcategory_attribute.unit)
            )
            .where(
                self.subcategory_attribute.subcategory_id == subcategory_id,
                self.subcategory_attribute.is_filterable == True
            )
        )

        query_result = await self._session.execute(statement)
        return query_result.scalars().all()


class SubcategoryRepository(AbstractSubcategoryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.category = Category
        self.subcategory = Subcategory

    async def get_rubric_by_subcategory(self, subcategory_id: UUID):
        statement = (
            select(self.subcategory)
            .options(
                joinedload(self.subcategory.category)
                .joinedload(self.category.rubric)
            )
            .where(self.subcategory.id == subcategory_id)
        )

        query_result = await self._session.execute(statement)
        return query_result.scalars().first()


class RegionRepository(AbstractRegionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.region = Region

    async def exists(self, region_id: UUID):
        statement = select(self.region).where(self.region.id == region_id)
        query_result = await self._session.execute(statement)
        return query_result.scalar_one_or_none() is not None

    async def get_all(self):
        statement = select(self.region)
        query_result = await self._session.execute(statement)
        return query_result.scalars().all()


class BrandRepository(AbstractBrandRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.brand = Brand

    async def get_all(self):
        statement = select(self.brand)
        query_result = await self._session.execute(statement)
        return query_result.scalars().all()

    async def get_by_id(self, brand_id: int):
        statement = select(self.brand).where(self.brand.id == brand_id)
        query_result = await self._session.execute(statement)
        return query_result.scalars().first()


class CountryRepository(AbstractCountryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.country = Country

    async def get_all(self):
        statement = select(self.country)
        query_result = await self._session.execute(statement)
        return query_result.scalars().all()


class ColorRepository(AbstractColorRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.color = Color

    async def get_all(self):
        statement = select(self.color)
        query_result = await self._session.execute(statement)
        return query_result.scalars().all()
