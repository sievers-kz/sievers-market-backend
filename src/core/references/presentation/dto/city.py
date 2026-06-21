from uuid import UUID

from src.core.shared.presentation.dto import DTO


class RegionShortResponse(DTO):
    id: UUID
    name: str


class CityResponse(DTO):
    id: UUID
    name: str
    region_id: UUID
    region: RegionShortResponse | None = None


class CreateCityRequest(DTO):
    name: str
    region_id: UUID


class UpdateCityRequest(DTO):
    name: str | None = None
    region_id: UUID | None = None
