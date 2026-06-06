from dependency_injector import containers, providers

from src.core.media.application.services.media_service import MediaService
from src.core.media.infrastructure.minio_service import MinioService
from src.core.media.infrastructure.uow import MediaUnitOfWork


class MediaContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()
    minio_config = providers.Configuration()
    minio_client = providers.Dependency()

    uow = providers.Factory(
        MediaUnitOfWork,
        session_factory=session_factory
    )

    minio_service = providers.Factory(
        MinioService,
        bucket_name=minio_config.bucket_name,
        client=minio_client
    )

    media_service = providers.Factory(
        MediaService,
        uow=uow,
        storage=minio_service,
    )
