import uuid

import pytest

from src.core.iam.domain.enums import OTPType, TokenType
from src.core.iam.domain.exceptions import AccountNotFoundError, InvalidTokenTypeError
from src.core.iam.presentation.dto import AccountConfirmation, LoginAccount, RefreshData
from src.core.shared.domain.exceptions import UnauthorizedError
from tests.iam.conftest import create_user_request, get_token_by_value


class TestRefreshTokenUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_refresh_token(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        refresh_token_usecase,
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
        response = await login_user_usecase.execute(login_dto)

        refresh_token = RefreshData(refresh_token=response.refresh_token)
        new_response = await refresh_token_usecase.execute(refresh_token)

        updated_user = await account_repository.get_account_by_email(dto.email)
        old_token = get_token_by_value(updated_user.tokens, response.refresh_token)

        assert old_token is not None
        assert old_token.is_revoked is True

        new_token = get_token_by_value(updated_user.tokens, new_response.refresh_token)
        assert new_token is not None
        assert new_token.is_revoked is False

        assert new_response.access_token is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_invalid_refresh_token(self, refresh_token_usecase):
        invalid_token = RefreshData(refresh_token="invalid_refresh_token")
        with pytest.raises(UnauthorizedError):
            await refresh_token_usecase.execute(invalid_token)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_ghost_token(self, refresh_token_usecase, token_service):
        fake_user_id = uuid.uuid4()
        generated_ghost_refresh_token = token_service.create_token(
            fake_user_id, TokenType.REFRESH
        )
        ghost_refresh_token_dto = RefreshData(
            refresh_token=generated_ghost_refresh_token.value
        )

        with pytest.raises(AccountNotFoundError):
            await refresh_token_usecase.execute(ghost_refresh_token_dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_wrong_token_type(
        self, refresh_token_usecase, token_service
    ):
        fake_user_id = uuid.uuid4()
        wrong_token = token_service.create_token(fake_user_id, TokenType.ACCESS)
        wrong_token_dto = RefreshData(refresh_token=wrong_token.value)

        with pytest.raises(InvalidTokenTypeError):
            await refresh_token_usecase.execute(wrong_token_dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_on_reused_revoked_token(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        refresh_token_usecase,
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
        login_response = await login_user_usecase.execute(login_dto)

        first_refresh_token_dto = RefreshData(
            refresh_token=login_response.refresh_token
        )
        await refresh_token_usecase.execute(first_refresh_token_dto)

        with pytest.raises(ValueError) as exc:
            await refresh_token_usecase.execute(first_refresh_token_dto)

        assert str(exc.value) == "Token is already revoked"
