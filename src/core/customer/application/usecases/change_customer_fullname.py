from uuid import UUID

from src.core.customer.presentation.dto import ChangeCustomerFullname
from src.core.customer.application.interfaces.uow import ICustomerUnitOfWork


class ChangeCustomerFullnameUseCase:
    def __init__(self, uow: ICustomerUnitOfWork):
        self.uow = uow

    async def execute(self, customer_id: UUID, fullname_data: ChangeCustomerFullname):
        async with self.uow as uow:
            customer = await uow.customer.get_by_id(customer_id)
            if customer is None:
                raise ValueError("Customer not found")

            customer.change_fullname(
                fullname_data.last_name,
                fullname_data.first_name,
                fullname_data.patronymic
            )

            await uow.customer.save(customer)
            await uow.commit()
