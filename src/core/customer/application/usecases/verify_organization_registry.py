from uuid import UUID

from src.core.customer.application.services.taxpayer_service import TaxpayerService
from src.core.customer.domain.enums import RegistryStatus
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class VerifyOrganizationRegistryUseCase:
    def __init__(self, uow: CustomerUnitOfWork, taxpayer_service: TaxpayerService):
        self.uow = uow
        self.taxpayer_service = taxpayer_service

    async def execute(self, organization_id: UUID) -> None:
        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None or organization.registry_status != RegistryStatus.PENDING:
                return
            kind, tax_id = organization.kind, organization.tax_id

        taxpayer = await self.taxpayer_service.verify(kind, tax_id)

        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None or organization.registry_status != RegistryStatus.PENDING:
                return

            if taxpayer is None:
                organization.mark_registry_not_found()
            else:
                organization.mark_registry_verified(taxpayer.legal_name, taxpayer.legal_address)

            await uow.organization.save(organization)
            await uow.commit()
