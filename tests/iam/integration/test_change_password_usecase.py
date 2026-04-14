import pytest

from src.core.iam.presentation.dto import AccountConfirmation, LoginAccount, ChangePasswordData
from src.core.iam.domain.enums import TokenType
from tests.iam.conftest import create_user_request, get_token_by_type


class TestChangePasswordUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_change_password(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        change_password_usecase,
        account_repository,
        password_hasher
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        email_token = get_token_by_type(user.tokens, TokenType.EMAIL)
        old_password_hash = user.password.value

        confirmation_dto = AccountConfirmation(confirm_token=email_token.value)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        new_raw_password = "new_raw_password"
        change_password_dto = ChangePasswordData(raw_password=dto.raw_password, new_password=new_raw_password)
        await change_password_usecase.execute(user.id, change_password_dto)

        user_after_change_password = await account_repository.get_account_by_email(dto.email)
        new_password_hash = user_after_change_password.password.value

        assert new_password_hash != old_password_hash
        assert user_after_change_password.password.verify(new_raw_password, password_hasher)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_wrong_old_password(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        change_password_usecase,
        account_repository,
        password_hasher
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        email_token = get_token_by_type(user.tokens, TokenType.EMAIL)

        confirmation_dto = AccountConfirmation(confirm_token=email_token.value)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        change_password_dto = ChangePasswordData(
            raw_password="wrong_password",
            new_password="new_super_secret"
        )

        with pytest.raises(Exception) as exc:
            await change_password_usecase.execute(user.id, change_password_dto)

        assert str(exc.value) == "Invalid password"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_revokes_all_sessions_after_password_change(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        change_password_usecase,
        account_repository,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        email_token = get_token_by_type(user.tokens, TokenType.EMAIL)

        confirmation_dto = AccountConfirmation(confirm_token=email_token.value)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        change_password_dto = ChangePasswordData(raw_password=dto.raw_password, new_password="new_super_secret")
        await change_password_usecase.execute(user.id, change_password_dto)

        user_after_password_change = await account_repository.get_account_by_email(dto.email)
        refresh_tokens = [token for token in user_after_password_change.tokens if token.type == TokenType.REFRESH]

        for token in refresh_tokens:
            assert token.is_revoked is True
