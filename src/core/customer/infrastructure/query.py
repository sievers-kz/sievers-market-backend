from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.customer.infrastructure.models import Customer
from src.core.customer.presentation.dto import CustomerProfileResponse
from src.core.iam.infrastructure.models import Account
from src.core.shared.infrastructure.services.query_service import QueryService


class CustomerQueryService(QueryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_me(self, customer_id: UUID) -> CustomerProfileResponse:
        statement = (
            select(
                Customer.id.label("customer_id"),
                Customer.last_name,
                Customer.first_name,
                Customer.patronymic,
                Customer.avatar_url,
                Account.email,
            )
            .join(Account, Customer.account_id == Account.id)
            .where(Customer.id == customer_id)
        )

        result = (await self._session.execute(statement)).mappings().one_or_none()

        if not result:
            return None
        return CustomerProfileResponse.model_validate(result)
