from uuid import UUID

from src.core.buyer.application.interfaces.abstract_buyer_service import AbstractBuyerService
from src.core.iam.application.interfaces.abstract_profile_creator import AbstractProfileCreator
from src.core.seller.application.interfaces.abstract_seller_service import AbstractSellerService


class ProfileCreatorAdapter(AbstractProfileCreator):
    def __init__(
        self,
        buyer_service: AbstractBuyerService,
        seller_service: AbstractSellerService
    ):
        self._strategies = {
            "buyer": buyer_service,
            "seller": seller_service
        }

    async def create(self, account_id: UUID, profile_data):
        role = profile_data.role
        if role not in self._strategies:
            raise ValueError("Invalid role")

        strategy = self._strategies[role]
        await strategy.create(account_id, profile_data)
