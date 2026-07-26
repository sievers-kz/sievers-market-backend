import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import AccountConfirmation
from src.core.shared.domain.exceptions import InvalidPhoneFormatError
from src.core.vendor.presentation.dto import ChangeContactPhoneRequest
from tests.iam.conftest import create_user_request
from tests.vendor.conftest import create_vendor_request


class TestChangeContactPhoneUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_contact_phone_success(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        register_vendor_usecase,
        change_contact_phone_usecase,
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

        vendor_before = await vendor_repository.get_by_account_id(account_id)
        change_contact_phone_dto = ChangeContactPhoneRequest(
            contact_phone="+77472006243"
        )
        await change_contact_phone_usecase.execute(
            vendor_before.id, change_contact_phone_dto
        )

        vendor_after = await vendor_repository.get_by_account_id(account_id)
        assert vendor_after.contact_phone is not None
        assert vendor_after.contact_phone != vendor_before.contact_phone

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_contact_phone_invalid_format_raises(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        register_vendor_usecase,
        change_contact_phone_usecase,
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

        vendor = await vendor_repository.get_by_account_id(account_id)
        change_contact_phone_dto = ChangeContactPhoneRequest(contact_phone="+123456789")

        with pytest.raises(InvalidPhoneFormatError):
            await change_contact_phone_usecase.execute(
                vendor.id, change_contact_phone_dto
            )
