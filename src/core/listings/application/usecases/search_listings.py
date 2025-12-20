from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class SearchListingsUseCase:
    def __init__(self, unit_of_work: AbstractListingReferenceUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, query_string: str):
        async with self.unit_of_work as uow:
            listings = await uow.listing_query.search_listings(query_string)
            return listings
