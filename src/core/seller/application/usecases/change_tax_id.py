from uuid import UUID

from src.api.seller.dto import TaxIDData
from src.core.seller.application.interfaces.abstract_seller_uow import AbstractSellerUnitOfWork


class ChangeTaxIDUseCase:
    def __init__(self, unit_of_work: AbstractSellerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID, tax_id_data: TaxIDData):
        async with self.unit_of_work as uow:
            seller = await uow.seller.get_by_account_id(account_id)
            seller.change_tax_id(tax_id_data.tax_id)

            await uow.seller.save(seller)
            await uow.commit()
