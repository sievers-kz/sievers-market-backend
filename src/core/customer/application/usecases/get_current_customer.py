from uuid import UUID

from src.api.customer.dto import CustomerResponse
from src.core.customer.application.interfaces.abstract_customer_uow import AbstractCustomerUnitOfWork


class GetCurrentCustomerUseCase:
    def __init__(self, unit_of_work: AbstractCustomerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID):
        async with self.unit_of_work as uow:
            customer = await uow.customer.get_by_account_id(account_id)
            if not customer:
                raise ValueError("Buyer not found")

            return CustomerResponse(
                last_name=customer.fullname.last_name,
                first_name=customer.fullname.first_name,
                patronymic=customer.fullname.patronymic,
                avatar_url=customer.avatar_url
            )
