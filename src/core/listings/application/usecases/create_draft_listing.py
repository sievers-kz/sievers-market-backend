from uuid import UUID

from src.api.listings.dto import CreateDraftListingDTO
from src.core.listings.infrastructure.factories import ListingFactory
from src.core.listings.application.abstract_listing_unit_of_work import AbstractListingUnitOfWork


class CreateDraftListingUseCase:
    def __init__(self, unit_of_work: AbstractListingUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, draft_listing_dto: CreateDraftListingDTO, author_id: UUID):
        async with self.unit_of_work as uow:
            listing = ListingFactory.create(draft_listing_dto, author_id)
            listing.draft()

            await uow.listing.save(listing)
            await uow.commit()
