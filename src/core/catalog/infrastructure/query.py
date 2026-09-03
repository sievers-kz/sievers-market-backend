from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only

from src.core.catalog.infrastructure.enums import CatalogStatus
from src.core.catalog.infrastructure.models import (
    Category,
    Rubric,
    Subcategory,
    SubcategoryAttribute,
)
from src.core.catalog.presentation.dto.catalog import (
    AttributeFieldResponse,
    AttributeGroupFieldsResponse,
    AttributeResponse,
    FilterableAttributeResponse,
    RubricResponse,
)
from src.core.shared.infrastructure.services.query_service import QueryService


class CatalogQueryService(QueryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_subcategory_attributes(self, subcategory_id: UUID) -> list:
        statement = (
            select(SubcategoryAttribute)
            .where(SubcategoryAttribute.subcategory_id == subcategory_id)
            .options(
                joinedload(SubcategoryAttribute.attribute),
                joinedload(SubcategoryAttribute.group),
                joinedload(SubcategoryAttribute.unit),
            )
        )

        query_result = await self._session.execute(statement)
        links = query_result.scalars().unique().all()

        groups_map: dict[UUID, AttributeGroupFieldsResponse] = {}
        for link in sorted(links, key=lambda lnk: lnk.group.position):
            group = link.group
            if group.id not in groups_map:
                groups_map[group.id] = AttributeGroupFieldsResponse(
                    key=group.key,
                    label=group.label,
                    position=group.position,
                    fields=[],
                )

            groups_map[group.id].fields.append(
                AttributeFieldResponse(
                    key=link.attribute.key,
                    label=link.attribute.label,
                    type=link.attribute.type,
                    required=link.required,
                    filterable=link.filterable,
                    unit=(
                        {"key": link.unit.key, "label": link.unit.label}
                        if link.unit
                        else None
                    ),
                    options=link.attribute.options,
                    source=link.attribute.source,
                )
            )

        return AttributeResponse(groups=list(groups_map.values()))

    async def get_filterable_attributes(self, subcategory_id: UUID) -> list:
        statement = (
            select(SubcategoryAttribute)
            .where(
                SubcategoryAttribute.subcategory_id == subcategory_id,
                SubcategoryAttribute.filterable.is_(True),
            )
            .options(
                joinedload(SubcategoryAttribute.attribute),
                joinedload(SubcategoryAttribute.unit),
            )
        )

        query_result = await self._session.execute(statement)
        links = query_result.scalars().unique().all()

        filters = []
        for link in links:
            filter_fields = AttributeFieldResponse(
                key=link.attribute.key,
                label=link.attribute.label,
                type=link.attribute.type,
                required=link.required,
                filterable=link.filterable,
                unit=(
                    {"key": link.unit.key, "label": link.unit.label}
                    if link.unit
                    else None
                ),
                options=link.attribute.options,
                source=link.attribute.source,
            )
            filters.append(filter_fields)

        return FilterableAttributeResponse(filters=filters)

    async def get_category_tree(self) -> list[RubricResponse]:
        statement = (
            select(Rubric)
            .options(
                load_only(Rubric.id, Rubric.name),
                joinedload(Rubric.categories).options(
                    load_only(Category.id, Category.rubric_id, Category.name),
                    joinedload(Category.subcategories).options(
                        load_only(
                            Subcategory.id, Subcategory.category_id, Subcategory.name
                        ),
                    ),
                ),
            )
            .where(Rubric.status == CatalogStatus.ACTIVE)
        )

        query_result = await self._session.execute(statement)
        results = query_result.scalars().unique().all()
        return TypeAdapter(list[RubricResponse]).validate_python(results)
