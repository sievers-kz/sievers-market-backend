from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload

from src.core.catalog.application.interfaces.query_service import ICatalogQueryService
from src.core.catalog.domain.enums import CatalogStatus
from src.core.catalog.infrastructure.models import Subcategory, Rubric, Category
from src.core.catalog.presentation.dto.catalog import AttributeResponse, RubricResponse
from src.core.catalog.presentation.dto.subcategory import Attribute


class CatalogQueryService(ICatalogQueryService):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_subcategory_attributes(self, subcategory_id: UUID) -> list[Attribute]:
        statement = (
            select(Subcategory, Rubric)
            .join(Category, Subcategory.category_id == Category.id)
            .join(Rubric, Category.rubric_id == Rubric.id)
            .options(
                load_only(Subcategory.attributes),
                load_only(Rubric.attributes),
            ).where(Subcategory.id == subcategory_id)
        )

        query_result = await self._session.execute(statement)
        result = query_result.first()
        subcategory, rubric = result

        return AttributeResponse(
            base_fields=rubric.attributes,
            dynamic_fields=subcategory.attributes,
        )

    async def get_category_tree(self) -> list[RubricResponse]:
        statement = (
            select(Rubric)
            .options(
                load_only(Rubric.id, Rubric.name),
                joinedload(Rubric.categories).options(
                    load_only(Category.id, Category.rubric_id, Category.name),
                    joinedload(Category.subcategories).options(
                        load_only(Subcategory.id, Subcategory.category_id, Subcategory.name),
                    )
                )
            ).where(Rubric.status == CatalogStatus.ACTIVE)
        )

        query_result = await self._session.execute(statement)
        results = query_result.scalars().unique().all()
        return TypeAdapter(list[RubricResponse]).validate_python(results)
