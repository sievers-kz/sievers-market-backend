import pytest

from src.api.auth.auth_dto import LoginUserDTO, RefreshTokenDTO
from src.api.auth.auth_dto import EmailConfirmationDTO
from src.core.auth.domain.exceptions.exception_classes import TokenCryptographyError, TokenAlreadyRevokedError


class TestRefreshTokenUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.create_user_usecase = container.create_user_usecase()
        self.email_confirmation_usecase = container.email_confirmation_usecase()
        self.login_user_usecase = container.login_user_usecase()
        self.refresh_token_usecase = container.refresh_token_usecase()
        self.uow = container.user_identity_unit_of_work()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_refresh_token_success(self, create_user_dto):
        dto = create_user_dto(email="test.refresh.token.success@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.user.email, raw_password=dto.credentials.raw_password)
        response = await self.login_user_usecase.execute(login_data)

        refresh_data = RefreshTokenDTO(refresh_token=response.refresh_token)
        response = await self.refresh_token_usecase.execute(refresh_data)

        async with self.uow:
            identity = await self.uow.identity.find_by_token_value(refresh_data.refresh_token)
            refresh_token = identity.get_token_by_value(refresh_data.refresh_token)
            assert refresh_token.is_revoked is True

        assert response.refresh_token is not None
        assert response.access_token is not None

        async with self.uow:
            identity = await self.uow.identity.find_by_token_value(response.refresh_token)
            refresh_token = identity.get_token_by_value(response.refresh_token)

            assert refresh_token is not None
            assert refresh_token.is_revoked is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_refresh_token_cryptography_fail(self, create_user_dto):
        dto = create_user_dto(email="test.refresh.token.cryptography.fail@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.user.email, raw_password=dto.credentials.raw_password)
        await self.login_user_usecase.execute(login_data)

        refresh_data = RefreshTokenDTO(refresh_token="nonexistsrefreshtoken")
        with pytest.raises(TokenCryptographyError):
            await self.refresh_token_usecase.execute(refresh_data)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_refresh_token_reuse_fail(self, create_user_dto):
        dto = create_user_dto(email="test.refresh.token.reuse.fail@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.user.email, raw_password=dto.credentials.raw_password)
        login_response = await self.login_user_usecase.execute(login_data)

        revoked_refresh_token = login_response.refresh_token
        first_refresh_data = RefreshTokenDTO(refresh_token=revoked_refresh_token)
        await self.refresh_token_usecase.execute(first_refresh_data)

        reuse_refresh_data = RefreshTokenDTO(refresh_token=revoked_refresh_token)
        with pytest.raises(TokenAlreadyRevokedError):
            await self.refresh_token_usecase.execute(reuse_refresh_data)

