import pytest

from src.api.auth.auth_dto import LoginUserDTO, RefreshTokenDTO
from src.api.users.user_dto import EmailConfirmationDTO
from src.core.auth.domain.exceptions.exception_classes import TokenStateError, TokenCryptographyError


class TestLogoutUserUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.create_user_usecase = container.create_user_usecase()
        self.login_user_usecase = container.login_user_usecase()
        self.email_confirmation_usecase = container.email_confirmation_usecase()
        self.logout_user_usecase = container.logout_user_usecase()
        self.uow = container.user_identity_unit_of_work()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_logout_user_success(self, create_user_dto):
        dto = create_user_dto(email="test.logout.success@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.email, raw_password="supersecret")
        response = await self.login_user_usecase.execute(login_data)

        logout_data = RefreshTokenDTO(refresh_token=response.refresh_token)
        await self.logout_user_usecase.execute(logout_data)

        async with self.uow:
            identity = await self.uow.identity.find_by_token_value(logout_data.refresh_token)
            assert identity is not None

            refresh_token_state = identity.get_token_by_value(logout_data.refresh_token)
            assert refresh_token_state.is_revoked is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_logout_user_double_request_fail(self, create_user_dto):
        dto = create_user_dto(email="test.logout.fail@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.email, raw_password="supersecret")
        response = await self.login_user_usecase.execute(login_data)

        logout_data = RefreshTokenDTO(refresh_token=response.refresh_token)
        await self.logout_user_usecase.execute(logout_data)

        with pytest.raises(TokenStateError):
            await self.logout_user_usecase.execute(logout_data)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_logout_user_token_cryptography_fail(self, create_user_dto):
        dto = create_user_dto(email="test.logout.token.cryptography.fail@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.email, raw_password="supersecret")
        await self.login_user_usecase.execute(login_data)

        logout_data = RefreshTokenDTO(refresh_token="nonexiststoken")
        with pytest.raises(TokenCryptographyError):
            await self.logout_user_usecase.execute(logout_data)

