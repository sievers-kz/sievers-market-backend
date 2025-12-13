from typing import List
from uuid import UUID

from src.api.listings.dto import UserListingsQueryDTO
from src.core.listings.domain.entities import Listing
from src.core.listings.domain.enums import ListingStatusEnum
from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class GetUserListingsUseCase:
    def __init__(self, unit_of_work: AbstractListingReferenceUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, status: ListingStatusEnum, author_id: UUID):
        async with self.unit_of_work as uow:
            listings: List[UserListingsQueryDTO] = await uow.listing_query.get_user_listings_by_status(status, author_id)
            return listings


