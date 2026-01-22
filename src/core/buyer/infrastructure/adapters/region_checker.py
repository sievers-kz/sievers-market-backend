from uuid import UUID

from src.core.buyer.application.interfaces.region_checker import AbstractRegionChecker
from src.core.references.application.interfaces.abstract_region_repository import AbstractRegionRepository


class RegionCheckerAdapter(AbstractRegionChecker):
    def __init__(self, repository: AbstractRegionRepository):
        self._repository = repository

    async def exists(self, region_id: UUID) -> bool:
        region = await self._repository.exists(region_id)
        if region:
            return True
        return False
