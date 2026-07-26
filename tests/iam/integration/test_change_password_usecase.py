import pytest

from src.core.iam.domain.enums import OTPType, TokenType
from src.core.iam.domain.exceptions import PasswordMismatchError
from src.core.iam.presentation.dto import (
    AccountConfirmation,
    ChangePasswordData,
    LoginAccount,
)
from tests.iam.conftest import create_user_request


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
        password_service,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{user.id}"
        )
        old_password_hash = user.password.value

        confirmation_dto = AccountConfirmation(
            account_id=user.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        new_raw_password = "new_raw_password"
        change_password_dto = ChangePasswordData(
            raw_password=dto.raw_password, new_password=new_raw_password
        )
        await change_password_usecase.execute(user.id, change_password_dto)

        user_after_change_password = await account_repository.get_account_by_email(
            dto.email
        )
        new_password_hash = user_after_change_password.password.value

        assert new_password_hash != old_password_hash
        assert password_service.verify(
            new_raw_password, user_after_change_password.password.value
        )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_wrong_old_password(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        change_password_usecase,
        account_repository,
        password_service,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{user.id}"
        )

        confirmation_dto = AccountConfirmation(
            account_id=user.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        change_password_dto = ChangePasswordData(
            raw_password="wrong_password", new_password="new_super_secret"
        )

        with pytest.raises(PasswordMismatchError):
            await change_password_usecase.execute(user.id, change_password_dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_revokes_all_sessions_after_password_change(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        change_password_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{user.id}"
        )

        confirmation_dto = AccountConfirmation(
            account_id=user.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        change_password_dto = ChangePasswordData(
            raw_password=dto.raw_password, new_password="new_super_secret"
        )
        await change_password_usecase.execute(user.id, change_password_dto)

        user_after_password_change = await account_repository.get_account_by_email(
            dto.email
        )
        refresh_tokens = [
            token
            for token in user_after_password_change.tokens
            if token.type == TokenType.REFRESH
        ]

        for token in refresh_tokens:
            assert token.is_revoked is True
