from datetime import timedelta

from minio import Minio

from src.core.media.application.interfaces.storage import IObjectStorage


class MinioService(IObjectStorage):
    def __init__(self, bucket_name: str, client: Minio):
        self._bucket_name = bucket_name
        self._client = client

    def generate_upload_url(self, object_name: str, expiration: int = 3600) -> str:
        return self._client.get_presigned_url(
            method="PUT",
            bucket_name=self._bucket_name,
            object_name=object_name,
            expires=timedelta(seconds=expiration)
        )

