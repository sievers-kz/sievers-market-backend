from uuid import UUID

from src.core.vendor.application.interfaces.uow import IVendorUnitOfWork
from src.core.vendor.domain.entities import Vendor
from src.core.vendor.presentation.dto import CreateVendorRequest


class CreateVendorUseCase:
    def __init__(self, uow: IVendorUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID, dto: CreateVendorRequest):
        async with self.uow as uow:
            current_vendor = await uow.vendor.get_by_tax_id(dto.tax_id)
            if current_vendor:
                raise ValueError("Такая компания уже зарегистрирована")

            new_vendor = Vendor.create(
                account_id=account_id,
                contact_last_name=dto.contact_last_name,
                contact_first_name=dto.contact_first_name,
                legal_name=dto.legal_name,
                legal_address=dto.legal_address,
                tax_id=dto.tax_id,
                legal_form=dto.legal_form,
            )

            await uow.vendor.save(new_vendor)
            await uow.commit()
