from uuid import UUID

from src.core.customer.application.interfaces.abstract_customer_repository import AbstractCustomerRepository
from src.core.customer.application.interfaces.abstract_customer_service import ICustomerService
from src.core.customer.domain.entities import Customer
from src.core.customer.infrastructure.factory import CustomerFactory


class CustomerService(ICustomerService):
    def __init__(self, repository: AbstractCustomerRepository):
        self._repository = repository

    async def create(self, account_id: UUID, last_name: str, first_name: str) -> Customer:
        buyer = CustomerFactory.create(account_id, last_name, first_name)
        await self._repository.save(buyer)
