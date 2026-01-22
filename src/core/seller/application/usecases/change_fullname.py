from uuid import UUID

from src.api.seller.dto import SellerFullnameData
from src.core.seller.application.interfaces.abstract_seller_uow import AbstractSellerUnitOfWork


class ChangeFullnameUseCase:
    def __init__(self, unit_of_work: AbstractSellerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID, fullname_data: SellerFullnameData):
        async with self.unit_of_work as uow:
            seller = await uow.seller.get_by_account_id(account_id)

            seller.change_fullname(
                fullname_data.last_name,
                fullname_data.first_name,
                fullname_data.patronymic
            )

            await uow.seller.save(seller)
            await uow.commit()
