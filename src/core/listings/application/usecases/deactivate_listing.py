from uuid import UUID

from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class DeactivateListingUseCase:
    def __init__(self, unit_of_work: AbstractListingReferenceUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, listing_id: UUID):
        async with self.unit_of_work as uow:
            listing = await uow.listing.get_listing_by_id(listing_id)
            listing.deactivate()

            await uow.listing.save(listing)
            await uow.commit()
