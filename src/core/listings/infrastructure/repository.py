import asyncio
from typing import List
from uuid import UUID

from sqlalchemy import select, delete, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.listings.dto import UserListingsQueryDTO, BaseFilters, DynamicFilters, ListingCards
from src.api.references.dto import SpecificationDTO
from src.core.listings.domain.enums import ListingStatusEnum
from src.core.listings.infrastructure.mappers import ListingMapper
from src.core.listings.infrastructure.models.listing import Listing as ORMListing, ListingMedia as ORMListingMedia
from src.core.references.domain.enums import MachinerySpecsValueTypeEnum
from src.core.references.infrastructure.models import (
    MachinerySubcategory as ORMSubcategory,
    MachinerySubcategorySpecification as ORMSubcategorySpecification
)
from src.core.listings.infrastructure.models.machinery import Machinery as ORMMachinery

from src.core.listings.domain.entities import (
    Listing as DomainListing,
    ListingMedia as DomainListingMedia,
    Machinery as DomainMachinery
)


class ListingRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.listing = ORMListing
        self.listing_media = ORMListingMedia
        self.machinery = ORMMachinery

    async def get_listing_by_id(self, listing_id: UUID) -> DomainListing:
        statement = (
            select(self.listing)
            .options(
                selectinload(self.listing.media),
                joinedload(self.listing.machinery)
            )
            .where(self.listing.id == listing_id)
        )

        result = await self._session.execute(statement)
        listing = result.scalar_one_or_none()

        if not listing:
            return None

        return ListingMapper.to_domain(listing)

    async def save(self, listing: DomainListing) -> None:
        await self._session.execute(
            delete(self.listing_media).where(
                self.listing_media.listing_id == listing.id
            )
        )
        await self._session.flush()

        mapped_listing = ListingMapper.to_orm(listing)
        await self._session.merge(mapped_listing)
        await self._session.flush()


class ListingQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.listing = ORMListing
        self.listing_media = ORMListingMedia
        self.machinery = ORMMachinery
        self.subcategory = ORMSubcategory

    async def get_filtered_listings(
        self,
        category_id: UUID,
        subcategory_id: UUID | None,
        min_price: int | None,
        max_price: int | None,
        page: int,
        page_size: int,
        applied_dynamic_filters: dict
    ):
        statement = (
            select(self.listing)
            .options(
                joinedload(self.listing.machinery)
                .joinedload(self.machinery.subcategory)
            )
            .options(
                selectinload(self.listing.media)
            )

            .join(self.machinery)
            .join(self.subcategory)

            .where(
                self.subcategory.category_id == category_id,
                self.listing.status == ListingStatusEnum.ACTIVE
            )
        )

        if subcategory_id is not None:
            statement = statement.where(self.subcategory.id == subcategory_id)

        if min_price is not None:
            statement = statement.where(self.listing.price >= min_price)

        if max_price is not None:
            statement = statement.where(self.listing.price <= max_price)

        if applied_dynamic_filters:
            statement = await self.apply_dynamic_filters(statement, applied_dynamic_filters)

        count_statement = select(func.count()).select_from(statement.subquery())
        total_result = await self._session.execute(count_statement)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        result = await self._session.execute(statement)
        listings = result.scalars().all()

        return [
            ListingCards(
                id=str(listing.id),
                title=listing.title,
                price=listing.price,
                media=listing.media[0].media_url if listing.media else None,
                status=listing.status,
                condition=listing.machinery.condition,
                subcategory=listing.machinery.subcategory.name,
                updated_at=listing.updated_at
            ) for listing in listings
        ], total

    async def apply_dynamic_filters(self, statement, applied_dynamic_filters: dict):
        base_filters = {"subcategory_id", "category_id", "min_price", "max_price", "sort_by", "page", "page_size"}

        for key, value in applied_dynamic_filters.items():
            if key in base_filters or key.endswith("_unit") or value in [None, ""]:
                continue

            base_key = key.replace("_min", "").replace("_max", "")
            unit_val = applied_dynamic_filters.get(f"{base_key}_unit")

            if key.endswith("_min"):
                condition, val = "(spec->>'value')::numeric >= :v", float(value)
            elif key.endswith("_max"):
                condition, val = "(spec->>'value')::numeric <= :v", float(value)
            else:
                condition, val = "spec->>'value' = ANY(:v)", (value if isinstance(value, list) else [value])

            statement = statement.where(
                text(f"""
                    EXISTS(
                        SELECT 1 FROM jsonb_array_elements(machinery.extra_specs) AS spec
                        WHERE spec->>'key' = :k_{key}
                            AND {condition.replace(':v', f':v_{key}')}
                            AND (CAST(:u_{key} AS TEXT) IS NULL OR spec->>'unit' = CAST(:u_{key} AS TEXT))
                    )
                """).bindparams(**{f"k_{key}": base_key, f"v_{key}": val, f"u_{key}": unit_val})
            )

        return statement

    async def get_user_listings_by_status(
        self,
        status: ListingStatusEnum,
        author_id: UUID
    ) -> List[UserListingsQueryDTO]:
        statement = (
            select(
                self.listing.id,
                self.listing.title,
                self.listing.price,
                self.listing.currency,
                self.listing.status,
                self.listing.updated_at,
                self.listing_media.media_url.label("media"),
                self.machinery.condition,
                self.subcategory.name.label("subcategory")
            )

            .outerjoin(
                self.machinery, self.machinery.listing_id == self.listing.id
            )
            .outerjoin(
                self.subcategory, self.subcategory.id == self.machinery.subcategory_id
            )

            .outerjoin(
                self.listing_media, (
                    (self.listing_media.listing_id == self.listing.id)
                    & (self.listing_media.position == 0)
                )
            )

            .where(
                self.listing.status == status,
                self.listing.author_id == author_id
            )

            .order_by(self.listing.updated_at.desc())
        )

        result = await self._session.execute(statement)
        return [UserListingsQueryDTO.model_validate(row, from_attributes=True) for row in result.all()]


class FilterQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.listing = ORMListing
        self.listing_media = ORMListingMedia
        self.machinery = ORMMachinery
        self.subcategory = ORMSubcategory
        self.subcategory_specification = ORMSubcategorySpecification

    async def get_base_filters(self, category_id: UUID):
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

    async def get_dynamic_filters(self, subcategory_id: UUID):
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