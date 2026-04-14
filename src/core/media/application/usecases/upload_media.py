from src.core.media.presentation.dto import UploadMediaDTO
from src.core.media.application.interfaces.abstract_media_uow import AbstractMediaUnitOfWork
from src.core.media.infrastructure.factory import MediaFactory


class UploadMediaUseCase:
    def __init__(self, unit_of_work: AbstractMediaUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, dto: UploadMediaDTO):
        async with self.unit_of_work as uow:
            current_max = await uow.media.get_max_position(dto.machinery_id)
            next_position = current_max + 1

            new_media_list = MediaFactory.create(dto, start_position=next_position)
            await uow.media.save(new_media_list)
            await uow.commit()
