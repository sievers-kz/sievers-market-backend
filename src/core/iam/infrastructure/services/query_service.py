from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.customer.infrastructure.models import Customer
from src.core.iam.infrastructure.models import Account
from src.core.iam.presentation.dto import (
    CustomerMeResponse,
    CustomerProfileResponse,
    MeResponse,
    NoRoleMeResponse,
    VendorMeResponse,
    VendorProfileResponse,
)
from src.core.vendor.infrastructure.models import Vendor


class GetMeQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_me(self, account_id: UUID) -> MeResponse:
        vendor_row = await self._get_vendor(account_id)
        if vendor_row is not None:
            return VendorMeResponse(
                profile=VendorProfileResponse.model_validate(vendor_row),
            )

        customer_row = await self._get_customer(account_id)
        if customer_row is not None:
            return CustomerMeResponse(
                profile=CustomerProfileResponse.model_validate(customer_row),
            )

        return NoRoleMeResponse()

    async def _get_vendor(self, account_id: UUID):
        statement = (
            select(
                Account.email,
                Account.password_changed_at,
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
                Vendor.logotype,
            )
            .join(Account, Vendor.account_id == Account.id)
            .where(
                Vendor.account_id == account_id,
                Vendor.closed_at.is_(None),
            )
        )
        return (await self._session.execute(statement)).mappings().one_or_none()

    async def _get_customer(self, account_id: UUID):
        statement = (
            select(
                Customer.id.label("customer_id"),
                Customer.last_name,
                Customer.first_name,
                Customer.patronymic,
                Customer.avatar_url,
                Account.email,
                Account.password_changed_at,
            )
            .join(Account, Customer.account_id == Account.id)
            .where(Customer.account_id == account_id)
        )
        return (await self._session.execute(statement)).mappings().one_or_none()
