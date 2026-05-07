import math
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.customer.infrastructure.models import Customer
from src.core.machinery.infrastructure.models import Machinery
from src.core.machinery.presentation.dto import MachineryCardQuery, PaginatedMachinery, MachineryDetailQuery, \
    MachineryOwner
from src.core.machinery.presentation.filters import MachineryFilter, MachineryOwnerFilter
from src.core.references.infrastructure.models import City, Brand, Color, Country
from src.core.catalog.infrastructure.models import Subcategory
from src.core.shared.domain.enums import ListingStatus


class MachineryQuery:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._machinery = Machinery

    async def get_machinery_list(self, filters: MachineryFilter, page: int, limit: int):
        statement = (
            select(
                self._machinery.id,
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                Subcategory.name.label("subcategory"),
                City.name.label("city"),
            )
            .select_from(self._machinery)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)
            .where(self._machinery.status == ListingStatus.ACTIVE)
        )

        filtered_statement = filters.filter(statement)
        count_stmt = select(func.count()).select_from(filtered_statement.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        offset = (page - 1) * limit
        paginated_stmt = (
            filtered_statement
            .order_by(self._machinery.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        query_result = await self._session.execute(paginated_stmt)
        items = [MachineryCardQuery(**row) for row in query_result.mappings().all()]
        pages_count = math.ceil(total / limit) if limit > 0 else 0

        return PaginatedMachinery(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages_count=pages_count
        )

    async def get_machinery_detail(self, machinery_id: UUID):
        statement = (
            select(
                self._machinery.id,
                Subcategory.name.label("subcategory"),
                Customer,
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                City.name.label("city"),
                self._machinery.description,
                Brand.name.label("brand"),
                self._machinery.model,
                self._machinery.year_of_issue,
                self._machinery.condition,
                Color.name.label("color"),
                Country.name.label("country"),
                self._machinery.attributes
            )

            .select_from(self._machinery)
            .join(Customer, self._machinery.customer_id == Customer.id)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)
            .join(Brand, self._machinery.brand_id == Brand.id)
            .outerjoin(Color, self._machinery.color_id == Color.id)
            .outerjoin(Country, self._machinery.country_id == Country.id)

            .where(
                self._machinery.id == machinery_id,
                self._machinery.status == ListingStatus.ACTIVE
            )
        )

        query_result = await self._session.execute(statement)
        mapped_result = query_result.mappings().first()

        if not mapped_result:
            return None

        return MachineryDetailQuery(
            **mapped_result,
            customer=MachineryOwner.model_validate(mapped_result["Customer"]),
        )

    async def get_customer_machinery(
        self,
        customer_id: UUID,
        filters: MachineryOwnerFilter,
        page: int,
        limit: int
    ):
        statement = (
            select(
                self._machinery.id,
                Subcategory.name.label("subcategory"),
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                City.name.label("city"),
            )

            .select_from(self._machinery)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)

            .where(
                self._machinery.customer_id == customer_id
            )
        )

        filtered_statement = filters.filter(statement)
        count_stmt = select(func.count()).select_from(filtered_statement.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        offset = (page - 1) * limit
        paginated_stmt = (
            filtered_statement
            .order_by(self._machinery.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        query_result = await self._session.execute(paginated_stmt)
        items = [MachineryCardQuery(**row) for row in query_result.mappings().all()]
        pages_count = math.ceil(total / limit) if limit > 0 else 0

        return PaginatedMachinery(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages_count=pages_count
        )
