from uuid import UUID

from src.api.buyer.dto import BuyerResponse
from src.core.buyer.application.interfaces.abstract_buyer_uow import AbstractBuyerUnitOfWork


class GetCurrentBuyerUseCase:
    def __init__(self, unit_of_work: AbstractBuyerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID):
        async with self.unit_of_work as uow:
            buyer = await uow.buyer.get_by_account_id(account_id)
            if not buyer:
                raise ValueError("Buyer not found")

            return BuyerResponse(
                last_name=buyer.fullname.last_name,
                first_name=buyer.fullname.first_name,
                patronymic=buyer.fullname.patronymic,
                avatar_url=buyer.avatar_url
            )
