from uuid import UUID

from src.core.wishlist.application.interfaces.abstract_wishlist_uow import AbstractWishlistUnitOfWork
from src.core.wishlist.domain.entities import Wishlist


class AddToWishlistUseCase:
    def __init__(self, unit_of_work: AbstractWishlistUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, customer_id: UUID, machinery_id: UUID):
        async with self.unit_of_work as uow:
            wishlist = Wishlist.create(customer_id=customer_id, machinery_id=machinery_id)
            await uow.wishlist.save(wishlist)
            await uow.commit()
