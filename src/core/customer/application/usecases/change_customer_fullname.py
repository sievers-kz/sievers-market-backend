from uuid import UUID
from venv import logger

from src.core.customer.presentation.dto import ChangeCustomerFullname
from src.core.customer.application.interfaces.uow import ICustomerUnitOfWork


class ChangeCustomerFullnameUseCase:
    def __init__(self, uow: ICustomerUnitOfWork):
        self.uow = uow

    async def execute(self, customer_id: UUID, fullname_data: ChangeCustomerFullname):
        async with self.uow as uow:
            customer = await uow.customer.get_by_id(customer_id)
            customer.change_fullname(
                fullname_data.last_name,
                fullname_data.first_name,
                fullname_data.patronymic
            )

            await uow.customer.save(customer)
            await uow.commit()

        logger.info("Fullname changed | customer_id={}", customer_id)
