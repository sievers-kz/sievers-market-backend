from typing import List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.listings.dto import UserListingsQueryDTO
from src.api.references.dto import SpecificationDTO
from src.core.listings.domain.enums import ListingStatusEnum
from src.core.listings.infrastructure.mappers import ListingMapper
from src.core.listings.infrastructure.models.listing import Listing as ORMListing, ListingMedia as ORMListingMedia
from src.core.references.infrastructure.models import MachinerySubcategory as ORMSubcategory
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