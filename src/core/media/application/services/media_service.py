import uuid
from uuid import UUID

from src.configuration.dependencies import media
from src.core.media.application.interfaces.storage import IObjectStorage
from src.core.media.application.interfaces.uow import IMediaUnitOfWork
from src.core.media.domain.entities import Media
from src.core.media.domain.value_objects import MediaSize
from src.core.media.presentation.dto import GenerateUploadUrlRequest, UploadUrlResponse, ConfirmUploadResponse, \
    ConfirmUploadRequest


class MediaService:
    def __init__(self, uow: IMediaUnitOfWork, storage: IObjectStorage):
        self.uow = uow
        self.storage = storage

    async def generate_upload_url(self, dto: GenerateUploadUrlRequest) -> list[UploadUrlResponse]:
        response = []

        for file in dto.files:
            unique_key = uuid.uuid4()
            object_key = f"uploads/{unique_key}/{file.client_filename}"

            upload_url = self.storage.generate_upload_url(object_name=object_key)
            response.append(
                UploadUrlResponse(
                    client_filename=file.client_filename,
                    upload_url=upload_url,
                    file_path=object_key
                )
            )

        return response

    async def confirm_upload(self, account_id: UUID, dto: ConfirmUploadRequest) -> list[ConfirmUploadResponse]:
        async with self.uow as uow:
            media_list = [
                Media.create(
                    owner_id=account_id,
                    media_url=item.file_path,
                    media_type=item.media_type,
                    media_size=MediaSize(item.media_size),
                )
                for item in dto.files
            ]

            await uow.media.save(media_list)
            await uow.commit()

            return [
                ConfirmUploadResponse(
                    media_id=media.id,
                    media_type=media.media_type,
                    media_size=media.media_size.value,
                )
                for media in media_list
            ]
