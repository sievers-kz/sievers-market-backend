from uuid import UUID

from sqlalchemy import select

from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.models import Customer, Organization
from src.core.customer.presentation.dto import CustomerMeResponse, OrganizationListResponse, OrganizationResponse
from src.core.iam.infrastructure.models import Account
from src.core.shared.infrastructure.services.query_service import QueryService


class CustomerQueryService(QueryService):
    def __init__(self, session):
        super().__init__(session=session)

    async def get_me(self, customer_id: UUID):
        statement = (
            select(
                Customer.id,
                Customer.last_name,
                Customer.first_name,
                Customer.patronymic,
                Account.email,
                Account.password_changed_at,
            )
            .join(Account, Account.id == Customer.account_id)
            .where(Customer.id == customer_id)
        )

        row = (await self._session.execute(statement)).one()

        return CustomerMeResponse(
            id=row.id,
            email=row.email,
            password_changed_at=row.password_changed_at,
            last_name=row.last_name,
            first_name=row.first_name,
            patronymic=row.patronymic,
        )

    async def get_organizations(self, owner_id: UUID) -> list[OrganizationListResponse]:
        statement = (
            select(
                Organization.id,
                Organization.tax_id,
                Organization.kind,
                Organization.registry_status,
                Organization.is_ownership_verified,
                Organization.legal_name,
                Organization.shop_name,
                Organization.logo_media_id,
            )
            .where(Organization.owner_id == owner_id)
            .order_by(Organization.created_at)
        )

        rows = (await self._session.execute(statement)).all()
        return [OrganizationListResponse.model_validate(row, from_attributes=True) for row in rows]

    async def get_organization(self, owner_id: UUID, organization_id: UUID) -> OrganizationResponse:
        statement = select(Organization).where(
            Organization.id == organization_id,
            Organization.owner_id == owner_id,
        )

        organization = (await self._session.execute(statement)).scalar_one_or_none()
        if organization is None:
            raise OrganizationNotFoundError()

        return OrganizationResponse.model_validate(organization)
