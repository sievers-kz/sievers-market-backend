import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import AccountConfirmation
from src.core.vendor.domain.enums import VendorStatus
from tests.iam.conftest import create_user_request
from tests.vendor.conftest import create_vendor_request


class TestCloseVendorUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_close_vendor_success(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        register_vendor_usecase,
        close_vendor_usecase,
        account_repository,
        vendor_repository,
        redis_service,
        customer_repository,
    ):
        create_account_dto = create_user_request()
        account_id = await create_user_usecase.execute(create_account_dto)

        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{account_id}"
        )
        account_confirmation_dto = AccountConfirmation(
            account_id=account_id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(account_confirmation_dto)

        create_vendor_dto = create_vendor_request()
        await register_vendor_usecase.execute(account_id, create_vendor_dto)

        vendor_before = await vendor_repository.get_by_account_id(account_id)
        await close_vendor_usecase.execute(vendor_before.id)

        vendor_after = await vendor_repository.get_by_account_id(account_id)
        assert vendor_after.status == VendorStatus.CLOSED

        customer = await customer_repository.get_by_account_id(vendor_before.account_id)
        assert customer is not None
        assert (
            customer.fullname.last_name
            == vendor_before.contact_fullname.contact_last_name
        )
