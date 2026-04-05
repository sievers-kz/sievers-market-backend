import pytest

from src.api.iam.dto import CreateUserRequest


class TestRegistrationUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_registration(
        self,
        create_user_usecase,
        account_repository,
        mock_notifier
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        email_token = user.tokens[0].value

        assert user is not None
        assert user.is_active is False
        assert user.password.value != dto.raw_password

        mock_notifier.send_confirmation_code.assert_called_once()
        mock_notifier.send_confirmation_code.assert_called_once_with(destination=dto.email, code=email_token)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_by_existing_user(self, create_user_usecase, account_repository, mock_notifier):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)
        mock_notifier.send_confirmation_code.reset_mock()

        with pytest.raises(Exception):
            await create_user_usecase.execute(dto)
        mock_notifier.send_confirmation_code.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_rollback_if_profile_creation_fails(
        self,
        create_user_usecase,
        account_repository,
        mock_notifier,
        mock_profile_creator
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        mock_profile_creator.create.side_effect = Exception("CRASH!")

        with pytest.raises(Exception, match="CRASH!"):
            await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        assert user is None

        mock_notifier.send_confirmation_code.assert_not_called()
