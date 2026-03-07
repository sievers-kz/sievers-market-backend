from uuid import UUID

from src.core.wishlist.application.interfaces.abstract_wishlist_repository import AbstractWishlistRepository


class WishlistService:
    def __init__(self, repository: AbstractWishlistRepository):
        self.repository = repository

    async def count_total_wishlist(self, machinery_id: UUID):
        return await self.repository.count_total_wishlist(machinery_id)
