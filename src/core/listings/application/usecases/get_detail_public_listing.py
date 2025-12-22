from uuid import UUID

from src.core.listings.application.abstract_listing_query_context import AbstractListingQueryContext


class GetDetailPublicListingUseCase:
    def __init__(self, query_service: AbstractListingQueryContext):
        self.query_service = query_service

    async def execute(self, listing_id: UUID):
        async with self.query_service as query:
            listing = await query.listing.get_detail_listing_by_id(listing_id)
            return listing

