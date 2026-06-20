import pytest

from src.core.customer.domain.entities import Customer


class TestCustomerRepository:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_customer_repository_saves_and_retrieves_customer(
        self, customer_repository, create_customer
    ):
        domain_customer = create_customer
        await customer_repository.save(domain_customer)
        saved_customer = await customer_repository.get_by_account_id(
            domain_customer.account_id
        )

        assert saved_customer is not None
        assert saved_customer.id == domain_customer.id
        assert isinstance(saved_customer, Customer)
