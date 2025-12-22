from uuid import UUID

from src.core.listings.application.abstract_listing_unit_of_work import AbstractListingUnitOfWork


class ActivateListingUseCase:
    def __init__(self, unit_of_work: AbstractListingUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, listing_id: UUID):
        async with self.unit_of_work as uow:
            listing = await uow.listing.get_listing_by_id(listing_id)
            listing.publish()

            await uow.listing.save(listing)
            await uow.commit()

