from uuid import UUID

from src.core.customer.domain.enums import RegistryStatus
from src.core.customer.domain.exceptions import OrganizationCannotBeDeletedError, OrganizationNotFoundError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class DeleteOrganizationUseCase:
    def __init__(self, uow: CustomerUnitOfWork):
        self.uow = uow

    async def execute(self, owner_id: UUID, organization_id: UUID) -> None:
        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None or organization.owner_id != owner_id:
                raise OrganizationNotFoundError()

            if organization.registry_status == RegistryStatus.VERIFIED:
                raise OrganizationCannotBeDeletedError()

            await uow.organization.delete(organization.id)
            await uow.commit()
