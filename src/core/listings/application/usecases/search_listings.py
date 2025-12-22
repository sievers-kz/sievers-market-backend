from src.core.listings.application.abstract_listing_query_context import AbstractListingQueryContext


class SearchListingsUseCase:
    def __init__(self, query_service: AbstractListingQueryContext):
        self.query_service = query_service

    async def execute(self, query_string: str):
        async with self.query_service as query:
            listings = await query.listing.search_listings(query_string)
            return listings
