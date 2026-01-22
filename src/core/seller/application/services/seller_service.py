from uuid import UUID

from src.core.seller.application.interfaces.abstract_seller_repository import AbstractSellerRepository
from src.core.seller.application.interfaces.abstract_seller_service import AbstractSellerService
from src.core.seller.domain.entities import Seller
from src.core.seller.infrastructure.factory import SellerFactory


class SellerService(AbstractSellerService):
    def __init__(self, repository: AbstractSellerRepository):
        self._repository = repository

    async def create(self, account_id: UUID, seller_data) -> Seller:
        seller = SellerFactory.create(account_id, seller_data)
        await self._repository.save(seller)
