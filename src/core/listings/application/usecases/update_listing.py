from uuid import UUID

from src.api.listings.dto import UpdateListingDTO
from src.core.listings.application.abstract_listing_unit_of_work import AbstractListingUnitOfWork


class UpdateListingUseCase:
    def __init__(self, unit_of_work: AbstractListingUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, update_listing_dto: UpdateListingDTO, listing_id: UUID):
        async with self.unit_of_work as uow:
            listing = await uow.listing.get_listing_by_id(listing_id)
            update_data = update_listing_dto.model_dump()

            listing.update(update_data)

            await uow.listing.save(listing)
            await uow.commit()
