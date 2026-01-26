import uuid
from src.api.media.dto import BatchPresignedUrlRequest, BatchPresignedUrlResponse, PresignedUrlResponseItem
from src.core.media.application.interfaces.abstract_object_storage import AbstractObjectStorage


class GetPreSignedUrlsUseCase:
    def __init__(self, object_storage: AbstractObjectStorage):
        self.object_storage = object_storage

    async def execute(self, command: BatchPresignedUrlRequest) -> BatchPresignedUrlResponse:
        response_items = []

        for file_req in command.files:
            unique_id = uuid.uuid4()
            object_key = f"uploads/{unique_id}/{file_req.client_file_name}"

            url = self.object_storage.generate_presigned_url(object_name=object_key,)

            response_items.append(
                PresignedUrlResponseItem(
                    client_file_name=file_req.client_file_name,
                    upload_url=url,
                    file_path=object_key
                )
            )

        return BatchPresignedUrlResponse(items=response_items)
