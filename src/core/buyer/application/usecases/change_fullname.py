from uuid import UUID

from src.api.buyer.dto import ChangeFullname
from src.core.buyer.application.interfaces.abstract_buyer_uow import AbstractBuyerUnitOfWork


class ChangeFullnameUseCase:
    def __init__(self, unit_of_work: AbstractBuyerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID, fullname_data: ChangeFullname):
        async with self.unit_of_work as uow:
            buyer = await uow.buyer.get_by_account_id(account_id)
            if buyer is None:
                raise ValueError("Buyer not found")

            buyer.change_fullname(
                fullname_data.last_name,
                fullname_data.first_name,
                fullname_data.patronymic
            )

            await uow.buyer.save(buyer)
            await uow.commit()
