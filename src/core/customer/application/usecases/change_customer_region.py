from uuid import UUID

from src.api.customer.dto import ChangeCustomerRegion
from src.core.customer.application.interfaces.abstract_customer_uow import AbstractCustomerUnitOfWork
from src.core.customer.application.interfaces.region_checker import AbstractRegionChecker


class ChangeCustomerRegionUseCase:
    def __init__(
        self,
        unit_of_work: AbstractCustomerUnitOfWork,
        region_checker: AbstractRegionChecker,
    ):
        self.unit_of_work = unit_of_work
        self.region_checker = region_checker

    async def execute(self, account_id: UUID, region_data: ChangeCustomerRegion):
        if not self.region_checker.exists(region_data.region_id):
            raise ValueError("Region not found")

        async with self.unit_of_work as uow:
            customer = await uow.customer.get_by_account_id(account_id)
            customer.change_region(region_data.region_id)

            await uow.customer.save(customer)
            await uow.commit()
