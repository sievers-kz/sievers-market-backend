from io import BytesIO
from typing import AsyncGenerator

import sentry_sdk
from minio import Minio
from rbloom import Bloom
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from scripts.bloom.generate_bloom import BLOOM_OBJECT_NAME, _bloom_hash


async def init_bloom(client: Minio, bucket_name: str) -> AsyncGenerator[Bloom, None]:
    response = client.get_object(bucket_name, BLOOM_OBJECT_NAME)
    try:
        data = response.read()
    finally:
        response.close()
        response.release_conn()

    bf = Bloom.load_bytes(data, _bloom_hash)
    yield bf


def init_sentry(
    dsn: str,
    environment: str,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.1,
):
    init = sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ]
    )

    yield init

    client = sentry_sdk.Hub.current.client
    client.close()


async def init_engine(url: str, echo: bool = False) -> AsyncGenerator[AsyncEngine, None]:
    async_engine = create_async_engine(url=url, echo=echo)
    yield async_engine
    await async_engine.dispose()
