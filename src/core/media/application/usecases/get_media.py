from uuid import UUID

from src.core.media.presentation.dto import MediaResponse
from src.core.media.application.interfaces.abstract_media_uow import AbstractMediaUnitOfWork


class GetMediaUseCase:
    def __init__(self, unit_of_work: AbstractMediaUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, machinery_id: UUID):
        async with self.unit_of_work as uow:
            media = await uow.media.get_media_by_machinery_id(machinery_id)
            return [MediaResponse.model_validate(m, from_attributes=True) for m in media]
