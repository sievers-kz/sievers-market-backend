from uuid import UUID

from src.core.customer.application.interfaces.uow import ICustomerUnitOfWork
from src.core.customer.domain.entities import Customer
from src.core.customer.presentation.dto import CreateCustomerRequest


class CreateCustomerUseCase:
    def __init__(self, uow: ICustomerUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID, dto: CreateCustomerRequest):
        async with self.uow as uow:
            new_customer = Customer.create(
                account_id=account_id,
                last_name=dto.last_name,
                first_name=dto.first_name,
            )

            await uow.customer.save(new_customer)
            await uow.commit()
