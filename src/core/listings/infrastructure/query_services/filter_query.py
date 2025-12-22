import asyncio
from typing import List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.listings.dto import BaseFilters, DynamicFilters
from src.core.listings.domain.enums import ListingStatusEnum
from src.core.listings.infrastructure.models.listing import Listing, ListingMedia
from src.core.listings.infrastructure.models.machinery import Machinery
from src.core.references.infrastructure.models import MachinerySubcategory, MachinerySubcategorySpecification


class FilterQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.listing = Listing
        self.listing_media = ListingMedia
        self.machinery = Machinery
        self.subcategory = MachinerySubcategory
        self.subcategory_specification = MachinerySubcategorySpecification

    async def get_base_filters(self, category_id: UUID) -> BaseFilters:
        subcategories_statement = (
            select(self.subcategory.id, self.subcategory.name)
            .where(self.subcategory.category_id == category_id)
        )

        prices_statement = (
            select(
                func.min(self.listing.price).label("min_price"),
                func.max(self.listing.price).label("max_price")
            )

            .join(self.machinery, self.machinery.listing_id == self.listing.id)
            .join(self.subcategory, self.subcategory.id == self.machinery.subcategory_id)

            .where(
                self.subcategory.category_id == category_id,
                self.listing.status == ListingStatusEnum.ACTIVE
            )
        )

        results = await asyncio.gather(
            self._session.execute(subcategories_statement),
            self._session.execute(prices_statement)
        )

        subcategories_result = results[0].all()
        price_result = results[1].one()

        return BaseFilters(
            subcategories=[
                {"id": str(sub.id), "name": sub.name}
                for sub in subcategories_result
            ],
            price_range={
                "min": price_result.min_price,
                "max": price_result.max_price
            }
        )

    async def get_dynamic_filters(self, subcategory_id: UUID) -> List[DynamicFilters]:
        statement = (
            select(self.subcategory_specification)
            .options(
                joinedload(self.subcategory_specification.subcategory),
                joinedload(self.subcategory_specification.specification),
                joinedload(self.subcategory_specification.unit)
            )
            .where(
                self.subcategory_specification.subcategory_id == subcategory_id,
                self.subcategory_specification.is_filterable == True
            )
        )

        results = await self._session.execute(statement)
        specs = results.scalars().all()

        return [
            DynamicFilters(
                key=spec.specification.key,
                label=spec.specification.label,
                type=spec.specification.value_type,
                unit={"name": spec.unit.name, "label": spec.unit.label} if spec.unit else None,
                options=[{"value": opt, "label": opt}
                    for opt in spec.specification.options
                ] if spec.specification.options else []
            ) for spec in specs
        ]