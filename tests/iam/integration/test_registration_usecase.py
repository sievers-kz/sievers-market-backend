import pytest

from src.core.iam.domain.enums import OTPType
from tests.iam.conftest import create_user_request


class TestRegistrationUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_registration(
        self,
        create_user_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")

        assert user is not None
        assert user.is_active is False
        assert user.password.value != dto.raw_password
        assert otp_code is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_by_existing_user(self, create_user_usecase, account_repository):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        with pytest.raises(ValueError, match="Пользователь с таким email уже существует"):
            await create_user_usecase.execute(dto)

