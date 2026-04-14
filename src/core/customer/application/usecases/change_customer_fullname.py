from uuid import UUID

from src.core.customer.presentation.dto import ChangeCustomerFullname
from src.core.customer.application.interfaces.abstract_customer_uow import AbstractCustomerUnitOfWork


class ChangeCustomerFullnameUseCase:
    def __init__(self, unit_of_work: AbstractCustomerUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, account_id: UUID, fullname_data: ChangeCustomerFullname):
        async with self.unit_of_work as uow:
            customer = await uow.customer.get_by_account_id(account_id)
            if customer is None:
                raise ValueError("Customer not found")

            customer.change_fullname(
                fullname_data.last_name,
                fullname_data.first_name,
                fullname_data.patronymic
            )

            await uow.customer.save(customer)
            await uow.commit()
