from uuid import UUID

from pydantic import Field

from src.core.media.domain.enums import MediaType
from src.core.shared.presentation.dto import DTO


class FileUploadInput(DTO):
    client_filename: str
    mime_type: MediaType


class GenerateUploadUrlRequest(DTO):
    files: list[FileUploadInput]


class UploadUrlResponse(DTO):
    client_filename: str
    upload_url: str
    file_path: str


class ConfirmUploadItem(DTO):
    file_path: str
    media_type: MediaType
    media_size: int = Field(description="Размер файла в байтах")


class ConfirmUploadRequest(DTO):
    files: list[ConfirmUploadItem]


class ConfirmUploadResponse(DTO):
    media_id: UUID
    media_type: MediaType
    media_size: int
