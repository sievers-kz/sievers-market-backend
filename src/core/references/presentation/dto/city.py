from uuid import UUID

from src.core.shared.presentation.dto import DTO


class CityResponse(DTO):
    id: UUID
    name: str


class CreateCityRequest(DTO):
    name: str


class UpdateCityRequest(DTO):
    name: str | None = None
