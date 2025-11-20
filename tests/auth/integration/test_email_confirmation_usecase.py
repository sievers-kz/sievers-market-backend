import pytest

from src.api.auth.auth_dto import EmailConfirmationDTO
from src.core.users.domain.exceptions.exception_classes import InvalidEmailConfirmationCodeError


class TestEmailConfirmationUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.create_user_usecase = container.create_user_usecase()
        self.email_confirmation_usecase = container.email_confirmation_usecase()
        self.uow = container.user_identity_unit_of_work()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_email_confirmation_success(self, create_user_dto):
        dto = create_user_dto()
        await self.create_user_usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)
            email_token = identity.tokens[0].token_value

        confirmation_data = EmailConfirmationDTO(confirmation_code=email_token)
        await self.email_confirmation_usecase.execute(confirmation_data)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            assert user.is_active is True

            identity = await self.uow.identity.get_user_identity(user.id)
            assert all(token.is_revoked for token in identity.tokens if token.token_value == email_token)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_email_confirmation_with_invalid_code(self):
        confirmation_data = EmailConfirmationDTO(confirmation_code="invalid_email_code")
        with pytest.raises(InvalidEmailConfirmationCodeError):
            await self.email_confirmation_usecase.execute(confirmation_data)

