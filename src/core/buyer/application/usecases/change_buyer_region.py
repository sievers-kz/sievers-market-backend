from uuid import UUID

from src.api.buyer.dto import ChangeBuyerRegion
from src.core.buyer.application.interfaces.abstract_buyer_uow import AbstractBuyerUnitOfWork
from src.core.buyer.application.interfaces.region_checker import AbstractRegionChecker


class ChangeBuyerRegionUseCase:
    def __init__(
        self,
        unit_of_work: AbstractBuyerUnitOfWork,
        region_checker: AbstractRegionChecker,
    ):
        self.unit_of_work = unit_of_work
        self.region_checker = region_checker

    async def execute(self, account_id: UUID, region_data: ChangeBuyerRegion):
        if not self.region_checker.exists(region_data.region_id):
            raise ValueError("Region not found")

        async with self.unit_of_work as uow:
            buyer = await uow.buyer.get_by_account_id(account_id)
            buyer.change_region(region_data.region_id)

            await uow.buyer.save(buyer)
            await uow.commit()
