from uuid import UUID

from src.core.customer.application.services.organization_service import OrganizationService
from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.uow import ListingUnitOfWork


class DeactivateListingUseCase:
    def __init__(
        self,
        uow: ListingUnitOfWork,
        listing_search_service: ListingSearchService,
        organization_service: OrganizationService,
    ):
        self.uow = uow
        self.listing_search_service = listing_search_service
        self.organization_service = organization_service

    async def execute(self, customer_id: UUID, listing_id: UUID):
        async with self.uow as uow:
            listing = await uow.listing.get_by_id(listing_id)
            if not listing or not await self.organization_service.is_owner(customer_id, listing.organization_id):
                raise ListingNotFoundError()

            listing.deactivate(listing.organization_id)
            await uow.listing.save(listing)
            await uow.commit()

        await self.listing_search_service.sync_listing(listing)
