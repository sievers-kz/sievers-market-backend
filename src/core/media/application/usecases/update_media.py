import uuid
from uuid import UUID

from src.core.media.presentation.dto import UpdateMediaDTO
from src.core.media.application.interfaces.abstract_media_uow import AbstractMediaUnitOfWork
from src.core.media.domain.entities import Media


class UpdateMediaUseCase:
    def __init__(self, unit_of_work: AbstractMediaUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, machinery_id: UUID, dto: UpdateMediaDTO):
        async with self.unit_of_work as uow:
            if dto.delete_ids:
                await uow.media.delete_by_ids(dto.delete_ids)

            if dto.append_files:
                current_max = await uow.media.get_max_position(machinery_id)
                start_position = current_max + 1

                new_media_entities = []
                for index, dto in enumerate(dto.append_files):
                    new_media = Media(
                        id=uuid.uuid4(),
                        machinery_id=machinery_id,
                        media_url=dto.file_path,
                        media_type=dto.mime_type,
                        media_size=dto.media_size,
                        position=start_position + index,
                    )
                    new_media_entities.append(new_media)

                await uow.media.save(new_media_entities)
            await uow.commit()
