from uuid import UUID

from src.core.vendor.application.interfaces.uow import IVendorUnitOfWork
from src.core.vendor.domain.entities import Vendor


class RestoreVendorUseCase:
    def __init__(self, uow: IVendorUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID):
        async with self.uow as uow:
            vendor: Vendor = await uow.vendor.get_by_account_id(account_id)
            vendor.restore()

            await uow.vendor.save(vendor)
            await uow.commit()
