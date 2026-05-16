from uuid import UUID

from src.core.listing.application.interfaces.uow import IListingUnitOfWork
from src.core.listing.presentation.dto import ChangeListingDescriptionRequest


class ChangeListingDescriptionUseCase:
    def __init__(self, uow: IListingUnitOfWork):
        self.uow = uow

    async def execute(self, listing_id: UUID, dto: ChangeListingDescriptionRequest):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing:
                raise ValueError(f"Listing {listing_id} not found")

            listing.change_description(listing.description)
            await uow.listing.save(listing)
            await uow.commit()
