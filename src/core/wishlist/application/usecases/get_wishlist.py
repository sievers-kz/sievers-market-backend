from uuid import UUID

from src.core.wishlist.application.interfaces.abstract_wishlist_uow import AbstractWishlistUnitOfWork


class GetWishlistUseCase:
    def __init__(self, unit_of_work: AbstractWishlistUnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self, buyer_id: UUID):
        async with self._unit_of_work as uow:
            wishlist = await uow.wishlist.get_by_buyer_id(buyer_id)
            return wishlist
