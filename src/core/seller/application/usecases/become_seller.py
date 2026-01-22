from uuid import UUID

from src.api.seller.dto import BecomeSellerRequest
from src.core.seller.application.interfaces.abstract_seller_uow import AbstractSellerUnitOfWork
from src.core.seller.infrastructure.factory import SellerFactory


class BecomeSellerUseCase:
    def __init__(self, unit_of_work: AbstractSellerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID, become_seller_data: BecomeSellerRequest):
        async with self.unit_of_work as uow:
            seller = await uow.seller.get_by_account_id(account_id)
            if seller:
                raise ValueError("Seller already exists")

            new_seller = SellerFactory.create(account_id, become_seller_data)

            await uow.seller.save(new_seller)
            await uow.commit()
