from uuid import UUID

from loguru import logger

from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.customer.presentation.dto import ChangeOrganizationContactEmailRequest


class ChangeOrganizationContactEmailUseCase:
    def __init__(self, uow: CustomerUnitOfWork):
        self.uow = uow

    async def execute(self, owner_id: UUID, organization_id: UUID, dto: ChangeOrganizationContactEmailRequest) -> None:
        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None or not organization.is_owned_by(owner_id):
                raise OrganizationNotFoundError()

            organization.change_contact_email(dto.contact_email)

            await uow.organization.save(organization)
            await uow.commit()

        logger.info("Organization contact email changed | organization_id={}", organization_id)
