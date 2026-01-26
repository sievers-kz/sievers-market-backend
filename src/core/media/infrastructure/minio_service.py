from datetime import timedelta

from minio import Minio

from src.core.media.application.interfaces.abstract_object_storage import AbstractObjectStorage


class MinioService(AbstractObjectStorage):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False
    ):
        self._bucket_name = bucket_name
        self._client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def generate_presigned_url(self, object_name: str, expiration: int = 3600):
        url = self._client.get_presigned_url(
            method="PUT",
            bucket_name=self._bucket_name,
            object_name=object_name,
            expires=timedelta(seconds=expiration)
        )

        return url
