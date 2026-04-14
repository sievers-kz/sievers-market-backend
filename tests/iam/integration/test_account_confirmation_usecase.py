from datetime import timedelta

import pytest
from freezegun import freeze_time

from src.core.iam.presentation.dto import CreateUserRequest, AccountConfirmation


class TestAccountConfirmationUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_account_confirmation(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        account_repository
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        unconfirmed_user = await account_repository.get_account_by_email(dto.email)
        confirm_token_value = unconfirmed_user.tokens[0].value
        assert unconfirmed_user.is_active is False

        confirmation_dto = AccountConfirmation(confirm_token=confirm_token_value)
        await account_confirmation_usecase.execute(confirmation_dto)

        confirmed_user = await account_repository.get_account_by_email(dto.email)
        assert confirmed_user.is_active is True

        revoked_token = confirmed_user.tokens[0]
        assert revoked_token.is_revoked is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_invalid_token(self, account_confirmation_usecase):
        confirmation_dto = AccountConfirmation(confirm_token="invalid_token")
        with pytest.raises(Exception):
            await account_confirmation_usecase.execute(confirmation_dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_expired_token(
        self,
        create_user_usecase,
        account_confirmation_usecase,
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

        with freeze_time() as frozen_time:
            frozen_time.tick(delta=timedelta(days=3))

            confirmation_dto = AccountConfirmation(confirm_token=token_value)
            with pytest.raises(Exception):
                await account_confirmation_usecase.execute(confirmation_dto)

        unconfirmed_user = await account_repository.get_account_by_email(dto.email)
        assert unconfirmed_user.is_active is False
