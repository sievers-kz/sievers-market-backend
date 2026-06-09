import pytest

from src.core.customer.presentation.dto import CreateCustomerRequest
from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import AccountConfirmation
from tests.iam.conftest import create_user_request


class TestCreateCustomerUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_success_create_customer(
        self,
        create_user_usecase,
        create_customer_usecase,
        account_confirmation_usecase,
        customer_repository,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        account_id = await create_user_usecase.execute(dto)

        otp_code = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{account_id}")
        confirmation_dto = AccountConfirmation(account_id=account_id, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        customer_dto = CreateCustomerRequest(last_name="Бисенов", first_name="Мейржан")
        await create_customer_usecase.execute(account_id, customer_dto)

        customer = await customer_repository.get_by_account_id(account_id)
        assert customer is not None
        assert customer.fullname.last_name == "Бисенов"

