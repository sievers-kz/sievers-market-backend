from uuid import UUID

from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class OrganizationService:
    """Public API of the customer context for questions about organizations (ADR 004).

    Other contexts (listing) ask here instead of reading customer's repositories.
    The rules themselves live in the Organization aggregate.
    """

    def __init__(self, uow: CustomerUnitOfWork):
        self.uow = uow

    async def ensure_can_publish(self, owner_id: UUID, organization_id: UUID) -> None:
        """Raise unless the organization belongs to `owner_id` and may publish listings."""
        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            if organization is None:
                raise OrganizationNotFoundError()
            organization.ensure_can_publish(owner_id)

    async def is_owner(self, owner_id: UUID, organization_id: UUID) -> bool:
        """Ownership only, no status check: an owner keeps managing listings whatever the registry says."""
        async with self.uow as uow:
            organization = await uow.organization.get_by_id(organization_id)
            return organization is not None and organization.is_owned_by(owner_id)
