from uuid import UUID

from src.core.buyer.application.interfaces.abstract_buyer_repository import AbstractBuyerRepository
from src.core.buyer.application.interfaces.abstract_buyer_service import AbstractBuyerService
from src.core.buyer.domain.entities import Buyer
from src.core.buyer.infrastructure.factory import BuyerFactory


class BuyerService(AbstractBuyerService):
    def __init__(self, repository: AbstractBuyerRepository):
        self._repository = repository

    async def create(self, account_id: UUID, buyer_data) -> Buyer:
        buyer = BuyerFactory.create(account_id, buyer_data)
        await self._repository.save(buyer)
