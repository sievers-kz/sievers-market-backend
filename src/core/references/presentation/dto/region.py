from uuid import UUID

from src.core.shared.presentation.dto import DTO


class CityShortResponse(DTO):
    id: UUID
    name: str


class RegionResponse(DTO):
    id: UUID
    name: str
    cities: list[CityShortResponse] = []


class CreateRegionRequest(DTO):
    name: str


class UpdateRegionRequest(DTO):
    name: str
