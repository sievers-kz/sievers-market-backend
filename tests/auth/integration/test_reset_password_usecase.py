import pytest

from src.api.auth.auth_dto import LoginUserDTO, ForgotPasswordDTO
from src.api.auth.auth_dto import EmailConfirmationDTO, ResetPasswordDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenAlreadyRevokedError


class TestResetPasswordUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.create_user_usecase = container.create_user_usecase()
        self.email_confirmation_usecase = container.email_confirmation_usecase()
        self.login_user_usecase = container.login_user_usecase()
        self.forgot_password_usecase = container.forgot_password_usecase()
        self.reset_password_usecase = container.reset_password_usecase()
        self.uow = container.user_identity_unit_of_work()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_reset_password_success(self, create_user_dto):
        dto = create_user_dto(email="test.reset.password.success@example.com",)
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.get_current_token(TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN)

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token.token_value)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.user.email, raw_password=dto.credentials.raw_password)
        await self.login_user_usecase.execute(login_data)

        forgot_password_data = ForgotPasswordDTO(email=dto.user.email)
        await self.forgot_password_usecase.execute(forgot_password_data)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            password_reset_token = identity.get_current_token(TokenTypeEnum.PASSWORD_RESET_TOKEN)

        password_reset_data = ResetPasswordDTO(
            reset_password_token=password_reset_token.token_value,
            new_password="new_password_reset_secret"
        )
        await self.reset_password_usecase.execute(password_reset_data)

        async with self.uow:
            identity = await self.uow.identity.get_user_identity(user.id)
            revoked_reset_token = identity.get_token_by_value(password_reset_token.token_value)
            assert revoked_reset_token.is_revoked is True

        login_with_new_password = LoginUserDTO(email=dto.user.email, raw_password=password_reset_data.new_password)
        login_response = await self.login_user_usecase.execute(login_with_new_password)

        assert login_response.refresh_token is not None
        assert login_response.access_token is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_reset_password_token_already_used_fail(self, create_user_dto):
        dto = create_user_dto(email="test.reset.password.token.already.used.fail@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.get_current_token(TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN)

        confirmation_token = EmailConfirmationDTO(confirmation_code=email_token.token_value)
        await self.email_confirmation_usecase.execute(confirmation_token)

        login_data = LoginUserDTO(email=dto.user.email, raw_password=dto.credentials.raw_password)
        await self.login_user_usecase.execute(login_data)

        forgot_password_data = ForgotPasswordDTO(email=dto.user.email)
        await self.forgot_password_usecase.execute(forgot_password_data)

        async with self.uow:
            identity = await self.uow.identity.get_user_identity(user.id)
            password_reset_token = identity.get_current_token(TokenTypeEnum.PASSWORD_RESET_TOKEN)

        reset_password_data = ResetPasswordDTO(
            reset_password_token=password_reset_token.token_value,
            new_password="first_secret_password"
        )
        await self.reset_password_usecase.execute(reset_password_data)

        reset_password_data_reuse = ResetPasswordDTO(
            reset_password_token=password_reset_token.token_value,
            new_password="first_secret_password"
        )

        with pytest.raises(TokenAlreadyRevokedError):
            await self.reset_password_usecase.execute(reset_password_data_reuse)

        login_with_new_password = LoginUserDTO(email=dto.user.email, raw_password="first_secret_password")
        login_response = await self.login_user_usecase.execute(login_with_new_password)

        assert login_response.refresh_token is not None
        assert login_response.access_token is not None
