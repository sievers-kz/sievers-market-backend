import pytest

from src.core.iam.presentation.dto import CreateUserRequest, AccountConfirmation, LoginAccount
from src.core.iam.domain.enums import TokenType, OTPType


class TestAccountLoginUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_account_login(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        account_repository,
        redis_service,
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")

        confirmation_dto = AccountConfirmation(account_id=user.id, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        response = await login_user_usecase.execute(login_dto)

        assert response.access_token is not None
        assert response.refresh_token is not None

        logged_in_user = await account_repository.get_account_by_email(dto.email)
        assert len(logged_in_user.tokens) == 1

        refresh_token = logged_in_user.tokens[0]
        assert refresh_token.type == TokenType.REFRESH
        assert refresh_token.value == response.refresh_token
        assert refresh_token.is_revoked is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_wrong_password(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        account_repository,
        login_user_usecase,
        redis_service,
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")

        confirmation_dto = AccountConfirmation(account_id=user.id, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        user_before_login = await account_repository.get_account_by_email(dto.email)
        tokens_count_before = len(user_before_login.tokens)

        login_dto = LoginAccount(email=dto.email, raw_password="wrong_password")
        with pytest.raises(Exception):
            await login_user_usecase.execute(login_dto)

        user_after_login = await account_repository.get_account_by_email(dto.email)
        assert len(user_after_login.tokens) == tokens_count_before

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_non_existent_email(self, login_user_usecase):
        login_dto = LoginAccount(email="ghost.mail@example.com", raw_password="super_secret")
        with pytest.raises(Exception):
            await login_user_usecase.execute(login_dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_unconfirmed_account(self, create_user_usecase, login_user_usecase):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        login_dto = LoginAccount(email=dto.email, raw_password="super_secret")
        with pytest.raises(Exception, match="Account is not confirmed"):
            await login_user_usecase.execute(login_dto)
