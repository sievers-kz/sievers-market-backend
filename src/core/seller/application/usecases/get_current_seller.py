from uuid import UUID

from src.api.seller.dto import SellerResponse
from src.core.seller.application.interfaces.abstract_seller_uow import AbstractSellerUnitOfWork


class GetCurrentSellerUseCase:
    def __init__(self, unit_of_work: AbstractSellerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID):
        async with self.unit_of_work as uow:
            seller = await uow.seller.get_by_account_id(account_id)
            if not seller:
                raise ValueError("Seller not found")

            return SellerResponse(
                last_name=seller.fullname.last_name,
                first_name=seller.fullname.first_name,
                patronymic=seller.fullname.patronymic,
                seller_type=seller.seller_type,
                legal_name=seller.legal_name.value,
                tax_id=seller.tax_id.value,
                logotype_url=seller.logotype_url
            )