from uuid import UUID

from src.core.listing.application.interfaces.uow import IListingUnitOfWork
from src.core.listing.domain.exceptions import ListingNotFoundError


class ActivateListingUseCase:
    def __init__(self, uow: IListingUnitOfWork):
        self.uow = uow

    async def execute(self, vendor_id: UUID, listing_id: UUID):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or listing.owner_id != vendor_id:
                raise ListingNotFoundError()

            listing.activate()
            await uow.listing.save(listing)
            await uow.commit()
