from typing import List
from uuid import UUID

from src.api.listings.dto import UserListingsQueryDTO
from src.core.listings.application.abstract_listing_query_context import AbstractListingQueryContext
from src.core.listings.domain.enums import ListingStatusEnum


class GetUserListingsUseCase:
    def __init__(self, query_service: AbstractListingQueryContext):
        self.query_service = query_service

    async def execute(self, status: ListingStatusEnum, author_id: UUID):
        async with self.query_service as query:
            listings: List[UserListingsQueryDTO] = await query.listing.get_user_listings_by_status(status, author_id)
            return listings


