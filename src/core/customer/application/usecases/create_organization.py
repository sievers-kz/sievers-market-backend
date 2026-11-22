from uuid import UUID

from loguru import logger

from src.core.customer.domain.entities import Organization
from src.core.customer.domain.exceptions import OrganizationAlreadyExistsError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.customer.presentation.dto import CreateOrganizationRequest, CreateOrganizationResponse
from src.core.shared.infrastructure.services.arq_service import ArqService
from src.core.shared.infrastructure.tasks import TaskNames


class CreateOrganizationUseCase:
    def __init__(self, uow: CustomerUnitOfWork, queue: ArqService):
        self.uow = uow
        self.queue = queue

    async def execute(self, owner_id: UUID, dto: CreateOrganizationRequest) -> CreateOrganizationResponse:
        async with self.uow as uow:
            if await uow.organization.get_by_tax_id(dto.tax_id):
                raise OrganizationAlreadyExistsError()

            new_organization = Organization.create(owner_id, dto.tax_id, dto.kind)
            await uow.organization.save(new_organization)
            await uow.commit()

        try:
            await self.queue.enqueue(
                task_name=TaskNames.VERIFY_ORGANIZATION_REGISTRY,
                organization_id=str(new_organization.id),
            )
        except Exception:
            # Redis моргнул: организация остаётся PENDING, её подберёт cron
            logger.exception("Failed to enqueue verification | organization_id={}", new_organization.id)

        return CreateOrganizationResponse(
            id=new_organization.id,
            registry_status=new_organization.registry_status,
        )
