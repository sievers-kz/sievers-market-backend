import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import CreateUserRequest, AccountConfirmation, LoginAccount, RefreshData
from tests.iam.conftest import create_user_request, get_token_by_value


class TestLogoutUserUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_logout_user(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        logout_user_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")

        confirmation_dto = AccountConfirmation(account_id=user.id, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        response = await login_user_usecase.execute(login_dto)

        refresh_token_request = RefreshData(refresh_token=response.refresh_token)
        await logout_user_usecase.execute(refresh_token_request)

        logged_out_user = await account_repository.get_account_by_email(dto.email)
        revoked_refresh_token = get_token_by_value(logged_out_user.tokens, refresh_token_request.refresh_token)

        assert revoked_refresh_token.is_revoked is True
