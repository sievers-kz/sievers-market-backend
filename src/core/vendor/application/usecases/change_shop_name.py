from uuid import UUID

from src.core.vendor.application.interfaces.uow import IVendorUnitOfWork
from src.core.vendor.domain.entities import Vendor
from src.core.vendor.presentation.dto import ChangeShopNameRequest


class ChangeShopNameUseCase:
    def __init__(self, uow: IVendorUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID, dto: ChangeShopNameRequest):
        async with self.uow as uow:
            vendor: Vendor = await uow.vendor.get_by_account_id(account_id)
            vendor.change_shop_name(dto.shop_name)

            await uow.vendor.save(vendor)
            await uow.commit()
