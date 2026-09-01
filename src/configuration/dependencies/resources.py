from typing import AsyncGenerator

import sentry_sdk
from meilisearch_python_sdk import AsyncClient
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def init_sentry(
    dsn: str,
    environment: str,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.1,
):
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            traces_sample_rate=traces_sample_rate,
            profiles_sample_rate=profiles_sample_rate,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ],
        )

    yield

    if dsn:
        sentry_sdk.flush()


async def init_engine(
    url: str, echo: bool = False
) -> AsyncGenerator[AsyncEngine, None]:
    async_engine = create_async_engine(url=url, echo=echo)
    yield async_engine
    await async_engine.dispose()


async def init_meilisearch(
    url: str,
    key: str,
):
    client = AsyncClient(url=url, api_key=key)
    try:
        yield client
    finally:
        await client.aclose()
