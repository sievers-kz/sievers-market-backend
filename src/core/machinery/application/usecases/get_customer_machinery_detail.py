from uuid import UUID

from src.core.machinery.application.interfaces.query import IMachineryQuery
from src.core.machinery.application.interfaces.wishlist_counter import IWishlistCounter


class GetCustomerMachineryDetailUseCase:
    def __init__(self, query: IMachineryQuery, wishlist_counter: IWishlistCounter):
        self.query = query
        self.wishlist_counter = wishlist_counter

    async def execute(self, customer_id: UUID, machinery_id: UUID):
        machinery_response = await self.query.get_machinery_detail(machinery_id)
        if not machinery_response:
            raise ValueError("Объявление не найдено. Возможно оно было помещено в архив или удалено")

        total_wishlist = await self.wishlist_counter.get_total_wishlist(machinery_id)
        enriched_response = machinery_response.model_copy(update={"wishlist_total_count": total_wishlist})
        return enriched_response
