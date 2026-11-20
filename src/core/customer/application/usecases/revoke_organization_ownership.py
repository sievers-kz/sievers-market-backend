from uuid import UUID

from loguru import logger

from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class RevokeOrganizationOwnershipUseCase:
    def __init__(self, uow: CustomerUnitOfWork):
        self.uow = uow

    async def execute(self, organization_id: UUID) -> None:
        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None:
                raise OrganizationNotFoundError()

            organization.revoke_ownership()

            await uow.organization.save(organization)
            await uow.commit()

        logger.info("Organization ownership revoked | organization_id={}", organization_id)
