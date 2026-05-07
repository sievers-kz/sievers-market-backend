from uuid import UUID

from src.core.references.application.interfaces.abstract_color_repository import IColorRepository
from src.core.references.application.interfaces.abstract_uow import IReferenceUnitOfWork
from src.core.references.domain.entities import Color
from src.core.references.presentation.dto.color import ColorResponse, CreateColorRequest, UpdateColorRequest


class ColorService:
    def __init__(self, uow: IReferenceUnitOfWork):
        self.uow = uow

    async def get_color_by_id(self, color_id: UUID):
        async with self.uow as uow:
            color = await uow.color.get_by_id(color_id)
            return ColorResponse.model_validate(color)

    async def get_color_list(self):
        async with self.uow as uow:
            color_list = await uow.color.get_all()
            return [ColorResponse.model_validate(color) for color in color_list]

    async def create_color(self, dto: CreateColorRequest) -> None:
        async with self.uow as uow:
            color = Color.create(name=dto.name, hex=dto.hex)
            await uow.color.save(color)
            await uow.commit()

    async def update_color(self, color_id: UUID, dto: UpdateColorRequest) -> None:
        async with self.uow as uow:
            color = await uow.color.get_by_id(color_id)
            color.update(name=dto.name, hex=dto.hex)

            await uow.color.save(color)
            await uow.commit()

    async def delete_color(self, color_id: UUID) -> None:
        async with self.uow as uow:
            await uow.color.delete(color_id)
            await uow.commit()
