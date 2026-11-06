import asyncio
from datetime import timedelta

import minio
from loguru import logger
from minio import Minio

from src.core.media.application.interfaces.storage import IObjectStorage
from src.core.media.domain.exceptions import MediaNotFoundError


class MinioService(IObjectStorage):
    """
    Работа с MinIO через два клиента.

    `client` подключается к MinIO по внутреннему адресу и выполняет реальные операции.
    `public_client` только подписывает ссылки под публичный адрес, который открывает браузер.
    Блокирующие вызовы клиента выполняются в потоке, чтобы не задерживать event loop.
    """

    def __init__(self, bucket_name: str, client: Minio, public_client: Minio):
        self._bucket_name = bucket_name
        self._client = client
        self._public_client = public_client

    def _ensure_bucket(self) -> None:
        if not self._client.bucket_exists(self._bucket_name):
            logger.warning("Не удалось найти бакет. Запущено автоматическое создание бакета")
            self._client.make_bucket(self._bucket_name)

    def _stat_object(self, object_name: str) -> None:
        try:
            self._client.stat_object(self._bucket_name, object_name)
        except minio.S3Error as err:
            if err.code in ("NoSuchBucket", "NoSuchKey"):
                raise MediaNotFoundError() from err
            raise

    def _presign(self, method: str, object_name: str, expiration: int) -> str:
        return self._public_client.get_presigned_url(
            method=method,
            bucket_name=self._bucket_name,
            object_name=object_name,
            expires=timedelta(seconds=expiration),
        )

    async def generate_upload_url(self, object_name: str, expiration: int = 3600) -> str:
        await asyncio.to_thread(self._ensure_bucket)
        return await asyncio.to_thread(self._presign, "PUT", object_name, expiration)

    async def generate_download_url(self, object_name: str, expiration: int = 3600) -> str:
        await asyncio.to_thread(self._stat_object, object_name)
        return await asyncio.to_thread(self._presign, "GET", object_name, expiration)
