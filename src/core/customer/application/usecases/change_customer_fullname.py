from uuid import UUID

from loguru import logger

from src.core.customer.domain.value_objects import Fullname
from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.customer.presentation.dto import ChangeCustomerFullname


class ChangeCustomerFullnameUseCase:
    def __init__(self, uow: CustomerUnitOfWork):
        self.uow = uow

    async def execute(self, customer_id: UUID, dto: ChangeCustomerFullname):
        async with self.uow as uow:
            customer = await uow.customer.get_by_id(customer_id)
            fullname = Fullname(last_name=dto.last_name, first_name=dto.first_name, patronymic=dto.patronymic)
            customer.change_fullname(fullname=fullname)

            await uow.customer.save(customer)
            await uow.commit()

        logger.info("Fullname changed | customer_id={}", customer_id)
