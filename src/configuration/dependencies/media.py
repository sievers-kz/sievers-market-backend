from dependency_injector import containers, providers

from src.core.media.application.usecases import GetPreSignedUrlsUseCase, UploadMediaUseCase, UpdateMediaUseCase, \
    GetMediaUseCase
from src.core.media.infrastructure.media_unit_of_work import MediaUnitOfWork
from src.core.media.infrastructure.minio_service import MinioService
from src.core.media.infrastructure.repository import MediaRepository


class MediaContainer(containers.DeclarativeContainer):
    object_storage_config = providers.Configuration()
    database_session = providers.Dependency()

    media_repository = providers.Factory(
        MediaRepository,
        session=database_session
    )

    media_unit_of_work = providers.Factory(
        MediaUnitOfWork,
        session=database_session
    )

    minio_service = providers.Factory(
        MinioService,
        endpoint=object_storage_config.object_storage_endpoint,
        access_key=object_storage_config.object_storage_access_key,
        secret_key=object_storage_config.object_storage_secret_key,
        bucket_name=object_storage_config.object_storage_bucket_name,
        secure=object_storage_config.object_storage_secure_config
    )

    generate_presigned_url_usecase = providers.Factory(
        GetPreSignedUrlsUseCase,
        object_storage=minio_service
    )

    upload_media_usecase = providers.Factory(
        UploadMediaUseCase,
        unit_of_work=media_unit_of_work
    )

    update_media_usecase = providers.Factory(
        UpdateMediaUseCase,
        unit_of_work=media_unit_of_work
    )

    get_media_usecase = providers.Factory(
        GetMediaUseCase,
        unit_of_work=media_unit_of_work
    )