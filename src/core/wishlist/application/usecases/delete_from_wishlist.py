from uuid import UUID

from src.core.wishlist.application.interfaces.abstract_wishlist_uow import AbstractWishlistUnitOfWork


class DeleteFromWishlistUseCase:
    def __init__(self, unit_of_work: AbstractWishlistUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, buyer_id: UUID, machinery_id: UUID):
        async with self.unit_of_work as uow:
            await uow.wishlist.delete(buyer_id, machinery_id)
            await uow.commit()
