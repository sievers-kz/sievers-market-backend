from uuid import UUID

from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.uow import ListingUnitOfWork


class DeleteListingUseCase:
    def __init__(self, uow: ListingUnitOfWork):
        self.uow = uow

    async def execute(self, organization_id: UUID, listing_id: UUID):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or listing.organization_id != organization_id:
                raise ListingNotFoundError()

            listing.delete(organization_id)
            await uow.listing.save(listing)
            await uow.commit()
