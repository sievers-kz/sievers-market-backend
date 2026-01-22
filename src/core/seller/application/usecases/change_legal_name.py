from uuid import UUID

from src.api.seller.dto import CompanyNameData
from src.core.seller.application.interfaces.abstract_seller_uow import AbstractSellerUnitOfWork


class ChangeCompanyNameUseCase:
    def __init__(self, unit_of_work: AbstractSellerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID, company_name_data: CompanyNameData):
        async with self.unit_of_work as uow:
            seller = await uow.seller.get_by_account_id(account_id)
            seller.change_company_name(company_name_data.company_name)

            await uow.seller.save(seller)
            await uow.commit()
