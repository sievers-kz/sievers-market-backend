import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import AccountConfirmation
from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.domain.exceptions import VendorAlreadyExistsError
from tests.iam.conftest import create_user_request
from tests.vendor.conftest import create_vendor_request


class TestCreateVendorUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_vendor_creation(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        register_vendor_usecase,
        account_repository,
        vendor_repository,
        redis_service,
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

        created_vendor = await vendor_repository.get_by_account_id(account_id)
        assert created_vendor is not None
        assert created_vendor.legal_form == LegalForm.IE

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_vendor_creation_already_exists(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        register_vendor_usecase,
        account_repository,
        vendor_repository,
        redis_service,
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

        with pytest.raises(VendorAlreadyExistsError):
            await register_vendor_usecase.execute(account_id, create_vendor_dto)
