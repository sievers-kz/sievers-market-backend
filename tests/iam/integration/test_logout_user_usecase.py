import pytest

from src.api.iam.dto import CreateUserRequest, AccountConfirmation, LoginAccount, RefreshData


class TestLogoutUserUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_logout_user(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        logout_user_usecase,
        account_repository
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        token_value = user.tokens[0].value

        confirmation_dto = AccountConfirmation(confirm_token=token_value)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        response = await login_user_usecase.execute(login_dto)

        refresh_token = RefreshData(refresh_token=response.refresh_token)
        await logout_user_usecase.execute(refresh_token)

        logged_out_user = await account_repository.get_account_by_email(dto.email)
        revoked_refresh_token = logged_out_user.tokens[1]

        assert revoked_refresh_token.is_revoked is True
