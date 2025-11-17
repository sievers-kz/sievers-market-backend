import pytest

from src.api.auth.auth_dto import LoginUserDTO
from src.api.users.user_dto import EmailConfirmationDTO
from src.core.auth.domain.exceptions.exception_classes import InvalidCredentialsError


class TestLoginUserUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.create_user_usecase = container.create_user_usecase()
        self.login_user_usecase = container.login_user_usecase()
        self.email_confirmation_usecase = container.email_confirmation_usecase()
        self.uow = container.user_identity_unit_of_work()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_login_user_success(self, create_user_dto):
        dto = create_user_dto(email="test.login@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        login_data = LoginUserDTO(email=dto.email, raw_password="supersecret")
        response = await self.login_user_usecase.execute(login_data)

        assert response.access_token is not None
        assert response.refresh_token is not None

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)

            refresh_token_exists = any(token.token_value == response.refresh_token for token in identity.tokens)
            assert refresh_token_exists is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_login_user_on_invalid_email(self, create_user_dto):
        dto = create_user_dto(email="test.fail.email@example.com")
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirm_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirm_data)

        wrong_login_data = LoginUserDTO(email="test.wrong.email@example.com", raw_password="supersecret")
        with pytest.raises(InvalidCredentialsError):
            await self.login_user_usecase.execute(wrong_login_data)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_login_user_on_invalid_password(self, create_user_dto):
        dto = create_user_dto(email="test.email@example.com", credentials={"raw_password": "supersecret"})
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirm_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirm_data)

        wrong_login_data = LoginUserDTO(email="test.email@example.com", raw_password="wrongpassword")
        with pytest.raises(InvalidCredentialsError):
            await self.login_user_usecase.execute(wrong_login_data)