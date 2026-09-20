from src.core.media.domain.exceptions import MediaNotFoundError
from src.core.shared.presentation.documentation import RouteDocs

GENERATE_UPLOAD_URL_DOC = RouteDocs(
    operation_id="generateUploadUrl",
    summary="Получение presigned URL для загрузки",
    description="""
        Генерирует presigned URL(-ы) MinIO/Silo для прямой загрузки файла(ов) с клиента, минуя backend.
    """,
    responses=(),
)

CONFIRM_UPLOAD_DOC = RouteDocs(
    operation_id="confirmUpload",
    summary="Подтверждение загрузки",
    description="""
        Подтверждает, что файл(ы) успешно загружены по presigned URL, и регистрирует медиа-объекты в системе.
    """,
    responses=(),
)

GET_MEDIA_DOC = RouteDocs(
    operation_id="getMedia",
    summary="Получение медиа-объекта",
    description="""
        Возвращает метаданные (или редиректит на публичный URL) медиа-объекта по идентификатору.
    """,
    responses=(MediaNotFoundError,),
)
