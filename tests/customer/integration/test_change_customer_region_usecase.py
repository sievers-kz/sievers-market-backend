import pytest

from src.core.customer.presentation.dto import (
    ChangeCustomerFullname,
    CreateCustomerRequest,
)
from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import AccountConfirmation
from tests.iam.conftest import create_user_request


class TestChangeCustomerFullnameUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_success_fullname_change(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        create_customer_usecase,
        change_customer_fullname_usecase,
        account_repository,
        customer_repository,
        redis_service,
    ):
        dto = create_user_request()
        email = await create_user_usecase.execute(dto)
        account = await account_repository.get_account_by_email(email)

        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{account.id}"
        )
        confirmation_dto = AccountConfirmation(email=email, confirm_code=otp_code)
        await account_confirmation_usecase.execute(confirmation_dto)

        customer_dto = CreateCustomerRequest(last_name="Testov", first_name="Test")
        await create_customer_usecase.execute(account.id, customer_dto)

        customer = await customer_repository.get_by_account_id(account.id)
        change_customer_fullname_dto = ChangeCustomerFullname(
            last_name="Bissenov", first_name="Meirzhan", patronymic="Basqaryly"
        )
        await change_customer_fullname_usecase.execute(
            customer.id, change_customer_fullname_dto
        )

        updated_customer = await customer_repository.get_by_id(customer.id)
        assert updated_customer.fullname.last_name == "Bissenov"
        assert updated_customer.fullname.first_name == "Meirzhan"
        assert updated_customer.fullname.patronymic == "Basqaryly"
