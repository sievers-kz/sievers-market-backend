from src.api.reference.dto import RegionDTO
from src.core.references.application.interfaces.abstract_region_repository import AbstractRegionRepository


class GetRegionsUseCase:
    def __init__(self, repository: AbstractRegionRepository):
        self.repository = repository

    async def execute(self):
        regions = await self.repository.get_all()
        return [RegionDTO.model_validate(region, from_attributes=True) for region in regions]
