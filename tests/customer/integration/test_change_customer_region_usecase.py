import pytest

from src.api.customer.dto import ChangeCustomerFullname
from tests.customer.conftest import create_customer, customer_repository


class TestChangeCustomerFullnameUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_customer_fullname_success(
        self,
        change_customer_fullname_usecase,
        customer_repository,
        create_customer
    ):
        created_customer = create_customer
        await customer_repository.save(created_customer)

        fullname_dto = ChangeCustomerFullname(last_name="Testov", first_name="Testovov", patronymic="Testovich")
        await change_customer_fullname_usecase.execute(created_customer.account_id, fullname_dto)

        changed_customer = await customer_repository.get_by_account_id(created_customer.account_id)
        assert changed_customer.fullname.last_name != created_customer.fullname.last_name

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_customer_fullname_fails_with_invalid_last_name(
        self,
        change_customer_fullname_usecase,
        create_customer,
        customer_repository
    ):
        created_customer = create_customer
        await customer_repository.save(created_customer)

        fullname_dto = ChangeCustomerFullname(
            last_name="WrongLastName123",
            first_name="Test",
            patronymic="Test"
        )

        with pytest.raises(ValueError, match="Invalid last name format"):
            await change_customer_fullname_usecase.execute(created_customer.account_id, fullname_dto)

