from uuid import UUID

from src.core.customer.application.interfaces.region_checker import AbstractRegionChecker
from src.core.references.application.interfaces.abstract_region_service import AbstractRegionService


class RegionCheckerAdapter(AbstractRegionChecker):
    def __init__(self, region_service: AbstractRegionService):
        self.region_service = region_service

    async def exists(self, region_id: UUID) -> bool:
        await self.region_service.exists(region_id)
