from uuid import UUID

from pydantic import BaseModel

from src.core.media.domain.enums import MediaType


class FilePresignedRequest(BaseModel):
    client_file_name: str
    mime_type: str


class BatchPresignedUrlRequest(BaseModel):
    files: list[FilePresignedRequest]


class PresignedUrlResponseItem(BaseModel):
    client_file_name: str
    upload_url: str
    file_path: str


class BatchPresignedUrlResponse(BaseModel):
    items: list[PresignedUrlResponseItem]


class MediaMetadata(BaseModel):
    file_path: str
    mime_type: MediaType
    media_size: int


class UploadMediaDTO(BaseModel):
    machinery_id: UUID
    files: list[MediaMetadata]


class UpdateMediaDTO(BaseModel):
    delete_ids: list[UUID] | None = None
    append_files: list[MediaMetadata]


class MediaResponse(BaseModel):
    id: UUID
    media_url: str
    media_type: MediaType
    media_size: int
    position: int
