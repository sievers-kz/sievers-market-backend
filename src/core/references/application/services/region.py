from uuid import UUID

from src.core.references.application.interfaces.abstract_region_repository import AbstractRegionRepository
from src.core.references.application.interfaces.abstract_region_service import AbstractRegionService


class RegionService(AbstractRegionService):
    def __init__(self, repository: AbstractRegionRepository):
        self._repository = repository

    async def exists(self, region_id: UUID) -> bool:
        await self._repository.exists(region_id)
