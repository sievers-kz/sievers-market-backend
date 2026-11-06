from unittest.mock import MagicMock

import minio
import pytest

from src.configuration.settings.settings import MinioConfig
from src.core.media.domain.exceptions import MediaNotFoundError
from src.core.media.infrastructure.minio_service import MinioService


@pytest.fixture
def clients():
    internal = MagicMock(name="internal")
    public = MagicMock(name="public")
    public.get_presigned_url.return_value = "https://media.example.com/signed"
    return internal, public


@pytest.fixture
def service(clients):
    internal, public = clients
    return MinioService(bucket_name="bucket", client=internal, public_client=public)


def _s3_error(code: str) -> minio.S3Error:
    return minio.S3Error(MagicMock(), code, "msg", "resource", "request", "host")


async def test_upload_url_is_signed_by_public_client(service, clients):
    internal, public = clients
    internal.bucket_exists.return_value = True

    url = await service.generate_upload_url("uploads/a/b.png")

    assert url == "https://media.example.com/signed"
    assert public.get_presigned_url.call_args.kwargs["method"] == "PUT"
    internal.get_presigned_url.assert_not_called()
    internal.make_bucket.assert_not_called()


async def test_upload_url_creates_missing_bucket_with_internal_client(service, clients):
    internal, public = clients
    internal.bucket_exists.return_value = False

    await service.generate_upload_url("uploads/a/b.png")

    internal.make_bucket.assert_called_once_with("bucket")
    public.make_bucket.assert_not_called()
    public.bucket_exists.assert_not_called()


async def test_download_url_checks_object_internally_and_signs_publicly(service, clients):
    internal, public = clients

    url = await service.generate_download_url("uploads/a/b.png")

    assert url == "https://media.example.com/signed"
    internal.stat_object.assert_called_once_with("bucket", "uploads/a/b.png")
    assert public.get_presigned_url.call_args.kwargs["method"] == "GET"
    public.stat_object.assert_not_called()


@pytest.mark.parametrize("code", ["NoSuchKey", "NoSuchBucket"])
async def test_download_url_raises_not_found_for_missing_object(service, clients, code):
    internal, public = clients
    internal.stat_object.side_effect = _s3_error(code)

    with pytest.raises(MediaNotFoundError):
        await service.generate_download_url("uploads/a/b.png")

    public.get_presigned_url.assert_not_called()


async def test_download_url_does_not_hide_other_storage_errors(service, clients):
    internal, _ = clients
    internal.stat_object.side_effect = _s3_error("AccessDenied")

    with pytest.raises(minio.S3Error):
        await service.generate_download_url("uploads/a/b.png")


_BASE = {
    "MINIO_ENDPOINT": "minio:9000",
    "MINIO_ROOT_USER": "user",
    "MINIO_ROOT_PASSWORD": "password",
    "MINIO_BUCKET_NAME": "bucket",
    "MINIO_SECURE_CONFIG": "false",
}


def _config(monkeypatch, **extra) -> MinioConfig:
    for key in ("MINIO_PUBLIC_ENDPOINT", "MINIO_PUBLIC_SECURE", "MINIO_REGION"):
        monkeypatch.delenv(key, raising=False)
    for key, value in {**_BASE, **extra}.items():
        monkeypatch.setenv(key, value)
    return MinioConfig(_env_file=None)


def test_public_settings_fall_back_to_internal(monkeypatch):
    config = _config(monkeypatch)

    assert config.public_endpoint == "minio:9000"
    assert config.public_secure is False
    assert config.region == "us-east-1"


def test_public_settings_are_independent_from_internal(monkeypatch):
    config = _config(
        monkeypatch,
        MINIO_PUBLIC_ENDPOINT="media.example.com",
        MINIO_PUBLIC_SECURE="true",
        MINIO_REGION="eu-west-1",
    )

    assert config.endpoint == "minio:9000"
    assert config.secure_config is False
    assert config.public_endpoint == "media.example.com"
    assert config.public_secure is True
    assert config.region == "eu-west-1"
