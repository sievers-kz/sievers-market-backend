import uuid

from src.core.media.presentation.dto import UploadMediaDTO
from src.core.media.domain.entities import Media


class MediaFactory:
    @staticmethod
    def create(dto: UploadMediaDTO, start_position: int = 0) -> list[Media]:
        return [
            Media(
                id=uuid.uuid4(),
                machinery_id=dto.machinery_id,
                media_url=file_item.file_path,
                media_type=file_item.mime_type,
                media_size=file_item.media_size,
                position=index
            )
            for index, file_item in enumerate(dto.files, start=start_position)
        ]
