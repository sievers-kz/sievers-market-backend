from typing import List
from uuid import UUID

from sqlalchemy import select, or_, desc, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.listings.dto import DetailListingResponse, ListingCards, UserListingsQueryDTO, InitialListingDataDTO
from src.core.listings.domain.enums import ListingStatusEnum
from src.core.listings.infrastructure.models.listing import Listing, ListingMedia
from src.core.listings.infrastructure.models.machinery import Machinery
from src.core.references.infrastructure.models import MachinerySubcategory


class ListingQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.listing = Listing
        self.listing_media = ListingMedia
        self.machinery = Machinery
        self.subcategory = MachinerySubcategory

    async def get_listing_by_id(self, listing_id: UUID):
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

        return InitialListingDataDTO.model_validate(listing, from_attributes=True)

    async def get_detail_listing_by_id(self, listing_id: UUID) -> DetailListingResponse:
        statement = (
            select(self.listing)
            .options(
                joinedload(self.listing.author),
                joinedload(self.listing.region),
                selectinload(self.listing.media),
                joinedload(self.listing.machinery)
                .options(
                    joinedload(self.machinery.subcategory),
                    joinedload(self.machinery.manufacturer),
                    joinedload(self.machinery.manufacturer_country),
                    joinedload(self.machinery.color)
                ),
            ).where(
                self.listing.id == listing_id,
                self.listing.status == ListingStatusEnum.ACTIVE
            )
        )

        result = await self._session.execute(statement)
        listing = result.unique().scalar_one_or_none()

        return DetailListingResponse.model_validate(listing, from_attributes=True)

    async def search_listings(self, query_string: str) -> List[ListingCards]:
        q_lower = query_string.strip().lower()
        words = q_lower.split()

        search_query = " & ".join([f"{word}:*" for word in words])
        ts_query = func.to_tsquery("russian", search_query)

        statement = (
            select(self.listing)
            .options(
                selectinload(self.listing.media),
                selectinload(self.listing.machinery).selectinload(self.machinery.subcategory)
            )
            .where(
                or_(
                    self.listing.search_vector.op("@@")(ts_query),
                    self.listing.search_content.op("%")(q_lower),
                )
            )
            .order_by(
                desc(func.ts_rank(self.listing.search_vector, ts_query)),
                desc(func.similarity(self.listing.search_content, q_lower))
            )
        )

        result = await self._session.execute(statement)
        listings = result.scalars().all()

        return [
            ListingCards(
                id=str(listing.id),
                title=listing.title or "Без названия",
                price=listing.price,
                media=listing.media[0].media_url if listing.media else None,
                status=listing.status,
                condition=listing.machinery.condition,
                subcategory=listing.machinery.subcategory.name,
                updated_at=listing.updated_at
            ) for listing in listings
        ]

    async def get_filtered_listings(
        self,
        category_id: UUID,
        subcategory_id: UUID | None,
        min_price: int | None,
        max_price: int | None,
        page: int,
        page_size: int,
        applied_dynamic_filters: dict
    ) -> List[ListingCards]:
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