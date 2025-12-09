from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.references.dto import SpecificationDTO
from src.core.listings.infrastructure.mappers import ListingMapper
from src.core.listings.infrastructure.models.listing import Listing as ORMListing, ListingMedia as ORMListingMedia
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

    async def save(self, listing: DomainListing) -> None:
        mapped_listing = ListingMapper.to_orm(listing)
        await self._session.merge(mapped_listing)
        await self._session.flush()

