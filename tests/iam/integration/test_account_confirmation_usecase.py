import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import InvalidOTPCodeError
from src.core.iam.presentation.dto import AccountConfirmation, CreateAccountRequest


class TestAccountConfirmationUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_account_confirmation(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        account_repository,
        redis_service,
    ):
        dto = CreateAccountRequest(
            email="test@example.com",
            raw_password="super_secret",
        )
        await create_user_usecase.execute(dto)

        unconfirmed_user = await account_repository.get_account_by_email(dto.email)
        assert unconfirmed_user.is_active is False

        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{unconfirmed_user.id}"
        )
        confirmation_dto = AccountConfirmation(
            account_id=unconfirmed_user.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        confirmed_user = await account_repository.get_account_by_email(dto.email)
        assert confirmed_user.is_active is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_invalid_code(
        self, create_user_usecase, account_confirmation_usecase, account_repository
    ):
        dto = CreateAccountRequest(
            email="test@example.com",
            raw_password="super_secret",
        )
        await create_user_usecase.execute(dto)

        account = await account_repository.get_account_by_email(dto.email)
        confirmation_dto = AccountConfirmation(
            account_id=account.id, confirm_code="123456"
        )

        with pytest.raises(InvalidOTPCodeError):
            await account_confirmation_usecase.execute(confirmation_dto)
