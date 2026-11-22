from uuid import UUID

from src.core.customer.domain.entities import Customer
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class GetOrCreateCustomerUseCase:
    def __init__(self, uow: CustomerUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID):
        async with self.uow as uow:
            customer = await uow.customer.get_by_account_id(account_id)
            if customer:
                return customer

            new_customer = Customer.create(account_id)
            await uow.customer.save(new_customer)
            await uow.commit()

        return new_customer
