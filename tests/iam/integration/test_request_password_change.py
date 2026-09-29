import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import PasswordMismatchError
from src.core.iam.presentation.dto import AccountConfirmation, LoginAccount, RequestPasswordChange
from tests.iam.conftest import create_user_request


class TestRequestPasswordChangeUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_request_password_change(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        request_password_change_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")
        old_password_hash = user.password.value

        confirmation_dto = AccountConfirmation(email=user.email.value, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        new_raw_password = "new_super_secret"
        request_password_change_dto = RequestPasswordChange(
            raw_password=dto.raw_password, new_password=new_raw_password
        )
        await request_password_change_usecase.execute(user.id, request_password_change_dto)

        user_after = await account_repository.get_account_by_id(user.id)
        assert user_after.password.value == old_password_hash

        password_otp_code = await redis_service.get(f"password_change:pending:{user.id}")
        assert password_otp_code is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_request_change_password_mismatch_password_failure(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        request_password_change_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")

        confirmation_dto = AccountConfirmation(email=user.email.value, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        request_password_change_dto = RequestPasswordChange(
            raw_password="wrong_password", new_password="new_super_secret"
        )
        with pytest.raises(PasswordMismatchError):
            await request_password_change_usecase.execute(user.id, request_password_change_dto)
