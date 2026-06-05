from uuid import UUID

from src.core.vendor.application.interfaces.uow import IVendorUnitOfWork
from src.core.vendor.domain.entities import Vendor
from src.core.vendor.presentation.dto import ChangeLogotypeRequest


class ChangeLogotypeUseCase:
    def __init__(self, uow: IVendorUnitOfWork):
        self.uow = uow

    async def execute(self, vendor_id: UUID, dto: ChangeLogotypeRequest):
        async with self.uow as uow:
            vendor: Vendor = await uow.vendor.get_by_id(vendor_id)
            vendor.change_logotype(dto.logotype)

            await uow.vendor.save(vendor)
            await uow.commit()
