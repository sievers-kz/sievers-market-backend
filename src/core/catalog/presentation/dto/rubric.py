from uuid import UUID

from src.core.shared.presentation.dto import DTO


class CreateRubricRequest(DTO):
    name: str


class ChangeRubricNameRequest(DTO):
    name: str


class RubricResponse(DTO):
    id: UUID
    name: str
