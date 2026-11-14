from uuid import UUID

from loguru import logger

from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.customer.presentation.dto import ChangeOrganizationContactPhoneRequest
from src.core.shared.domain.exceptions import InvalidPhoneFormatError
from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer


class ChangeOrganizationContactPhoneUseCase:
    def __init__(self, uow: CustomerUnitOfWork, phone_normalizer: PhoneNormalizer):
        self.uow = uow
        self.phone_normalizer = phone_normalizer

    async def execute(self, owner_id: UUID, organization_id: UUID, dto: ChangeOrganizationContactPhoneRequest) -> None:
        # `normalize` raises a bare ValueError when the input cannot be parsed at all.
        try:
            contact_phone = self.phone_normalizer.normalize(dto.contact_phone)
        except ValueError as exc:
            raise InvalidPhoneFormatError() from exc

        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None or not organization.is_owned_by(owner_id):
                raise OrganizationNotFoundError()

            organization.change_contact_phone(contact_phone)

            await uow.organization.save(organization)
            await uow.commit()

        logger.info("Organization contact phone changed | organization_id={}", organization_id)
