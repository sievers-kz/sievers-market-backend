import asyncio
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.api.references.dto import RoubricResponse, ManufacturerDTO, ManufactureCountryDTO, RegionDTO, ColorDTO, \
    AllReferencesDTO, SpecificationDTO
from src.core.references.infrastructure.models import Roubric, MachinerySubcategory, MachineryManufacturer, \
    MachineryCategory, MachineryManufacturerCountry, Region, Color, MachinerySpecification, \
    MachinerySubcategorySpecification


class ReferenceQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.roubric = Roubric
        self.category = MachineryCategory
        self.subcategory = MachinerySubcategory
        self.manufacturer = MachineryManufacturer
        self.manufacture_country = MachineryManufacturerCountry
        self.region = Region
        self.color = Color

    async def get_common_lookups(self):
        manufacturers_statement = select(self.manufacturer)
        manufacture_countries_statement = select(self.manufacture_country)
        regions_statement = select(self.region)
        colors_statement = select(self.color)

        results = await asyncio.gather(
            self._session.execute(manufacturers_statement),
            self._session.execute(manufacture_countries_statement),
            self._session.execute(regions_statement),
            self._session.execute(colors_statement)
        )

        manufacturers = [
            ManufacturerDTO.model_validate(manufacturer, from_attributes=True)
            for manufacturer in results[0].scalars().all()
        ]
        manufacture_countries = [
            ManufactureCountryDTO.model_validate(manufacture_country, from_attributes=True)
            for manufacture_country in results[1].scalars().all()
        ]
        regions = [
            RegionDTO.model_validate(region, from_attributes=True)
            for region in results[2].scalars().all()
        ]
        colors = [
            ColorDTO.model_validate(color, from_attributes=True)
            for color in results[3].scalars().all()
        ]

        return AllReferencesDTO(
            manufacturers=manufacturers,
            manufacture_countries=manufacture_countries,
            regions=regions,
            colors=colors
        )


class CategoryQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.roubric = Roubric
        self.category = MachineryCategory
        self.subcategory = MachinerySubcategory

    async def get_category_tree(self):
        statement = (
            select(self.roubric)
            .options(
                selectinload(
                    self.roubric.categories
                ).selectinload(
                    self.category.subcategories
                )
            )
        )

        result = await self._session.execute(statement)
        tree = result.unique().scalars().first()

        if not tree:
            return None

        return RoubricResponse.model_validate(tree, from_attributes=True)


class SpecificationQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.subcategory_specification = MachinerySubcategorySpecification

    async def get_subcategory_specifications(self, subcategory_id: UUID):
        statement = (
            select(self.subcategory_specification)
            .where(self.subcategory_specification.subcategory_id == subcategory_id)
            .options(
                joinedload(self.subcategory_specification.specification),
                joinedload(self.subcategory_specification.unit)
            )
        )

        result = await self._session.execute(statement)
        rows = result.scalars().all()

        return [
            SpecificationDTO(
                id=row.specification.id,
                key=row.specification.key,
                label=row.specification.label,
                value_type=row.specification.value_type,
                unit=row.unit.name if row.unit else None,
                position=row.specification.position,
                is_required=row.is_required,
                options=row.specification.options
            ) for row in rows
        ]
