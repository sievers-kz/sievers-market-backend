from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.iam.infrastructure.models import Account
from src.core.shared.infrastructure.services.query_service import QueryService
from src.core.vendor.infrastructure.models import Vendor
from src.core.vendor.presentation.dto import VendorProfileResponse


class VendorQueryService(QueryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_me(self, vendor_id: UUID) -> VendorProfileResponse:
        statement = (
            select(
                Account.email,
                Vendor.account_id,
                Vendor.id.label("vendor_id"),
                Vendor.is_verified,
                Vendor.contact_last_name,
                Vendor.contact_first_name,
                Vendor.contact_patronymic,
                Vendor.contact_phone,
                Vendor.legal_name,
                Vendor.legal_address,
                Vendor.tax_id,
                Vendor.legal_form,
                Vendor.shop_name,
                Vendor.logotype
            )
            .join(Account, Vendor.account_id == Account.id)
            .where(Vendor.id == vendor_id)
        )

        result = (await self._session.execute(statement)).mappings().one_or_none()
        if not result:
            return None
        return VendorProfileResponse.model_validate(result)

