from uuid import UUID

from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer
from src.core.vendor.application.interfaces.uow import IVendorUnitOfWork
from src.core.vendor.domain.entities import Vendor
from src.core.vendor.presentation.dto import ChangeContactPhoneRequest


class ChangeContactPhoneUseCase:
    def __init__(self, uow: IVendorUnitOfWork, phone_normalizer: PhoneNormalizer):
        self.uow = uow
        self.phone_normalizer = phone_normalizer

    async def execute(self, account_id: UUID, dto: ChangeContactPhoneRequest):
        async with self.uow as uow:
            vendor: Vendor = await uow.vendor.get_by_account_id(account_id)
            normalized_phone = self.phone_normalizer.normalize(dto.contact_phone)
            vendor.change_contact_phone(normalized_phone)

            await uow.vendor.save(vendor)
            await uow.commit()
