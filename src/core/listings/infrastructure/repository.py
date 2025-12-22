from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core.listings.infrastructure.mappers import ListingMapper
from src.core.listings.infrastructure.models.listing import Listing as ORMListing, ListingMedia as ORMListingMedia
from src.core.listings.infrastructure.models.machinery import Machinery as ORMMachinery

from src.core.listings.domain.entities import (
    Listing as DomainListing,
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


