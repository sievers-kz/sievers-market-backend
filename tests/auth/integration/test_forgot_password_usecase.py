from unittest.mock import AsyncMock

import pytest

from src.api.auth.auth_dto import LoginUserDTO, ForgotPasswordDTO
from src.api.users.user_dto import EmailConfirmationDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.users.domain.value_objects import Email


class TestForgotPasswordUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.create_user_usecase = container.create_user_usecase()
        self.email_confirmation_usecase = container.email_confirmation_usecase()
        self.login_user_usecase = container.login_user_usecase()
        self.email_sender = AsyncMock()
        self.forgot_password_usecase = container.forgot_password_usecase()
        self.uow = container.user_identity_unit_of_work()
        self.forgot_password_usecase.email_sender = self.email_sender

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_forgot_password_success(self, create_user_dto):
        dto = create_user_dto(email="test.forgot.password.success@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.get_current_token(TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN)

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token.token_value)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.email, raw_password=dto.credentials.raw_password)
        await self.login_user_usecase.execute(login_data)

        forgot_password_data = ForgotPasswordDTO(email=dto.email)
        await self.forgot_password_usecase.execute(forgot_password_data)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            password_reset_token = identity.get_current_token(TokenTypeEnum.PASSWORD_RESET_TOKEN)

            assert password_reset_token.token_value is not None
            assert password_reset_token.is_revoked is False

        email_value_object = Email.from_raw(raw_email=dto.email)
        self.email_sender.send_password_reset_confirmation.assert_awaited_once_with(
            to_email=email_value_object,
            template_data={
                "reset_password_token": password_reset_token.token_value
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_forgot_password_user_not_found_safe_exit(self):
        non_existent_email = "nonexistent.test@example.com"
        forgot_password_data = ForgotPasswordDTO(email=non_existent_email)

        await self.forgot_password_usecase.execute(forgot_password_data)
        self.email_sender.send_password_reset_confirmation.assert_not_called()

        async with self.uow:
            user = await self.uow.user.get_by_user_email(non_existent_email)
            assert user is None
