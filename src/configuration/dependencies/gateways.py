from arq import create_pool
from arq.connections import RedisSettings
from dependency_injector import containers, providers
from minio import Minio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from scripts.bloom.load_bloom import load_bloom
from src.configuration.database.connection import get_database_session
from src.configuration.dependencies.resources import (
    init_engine,
    init_meilisearch,
    init_sentry,
)
from src.core.shared.infrastructure.services.email_sender import SendGridEmailSender


class GatewaysContainer(containers.DeclarativeContainer):
    database_config = providers.Configuration()
    sendgrid_config = providers.Configuration()
    redis_config = providers.Configuration()
    minio_config = providers.Configuration()
    sentry_config = providers.Configuration()
    meilisearch_config = providers.Configuration()

    async_engine = providers.Resource(
        init_engine, url=database_config.database_url, echo=False
    )

    session_factory = providers.Singleton(
        async_sessionmaker, bind=async_engine, expire_on_commit=False, autoflush=False
    )

    database_session = providers.Resource(
        get_database_session, session_factory=session_factory
    )

    sendgrid_sender = providers.Singleton(
        SendGridEmailSender,
        api_key=sendgrid_config.api_key,
        from_email=sendgrid_config.from_email,
    )

    redis_client = providers.Singleton(
        Redis,
        host=redis_config.host,
        port=redis_config.port,
        db=redis_config.db,
        password=redis_config.password,
        decode_responses=True,
    )

    arq_redis_settings = providers.Singleton(
        RedisSettings,
        host=redis_config.host,
        port=redis_config.port,
        database=redis_config.database,
        password=redis_config.password,
    )

    arq_pool = providers.Singleton(
        create_pool,
        settings_=arq_redis_settings,
    )

    minio_client = providers.Singleton(
        Minio,
        endpoint=minio_config.endpoint,
        access_key=minio_config.access_key,
        secret_key=minio_config.secret_key,
        secure=minio_config.secure_config,
    )

    bloom_filter = providers.Singleton(load_bloom)

    sentry = providers.Resource(
        init_sentry,
        dsn=sentry_config.dsn,
        environment=sentry_config.mode,
        traces_sample_rate=sentry_config.traces_sample_rate,
        profiles_sample_rate=sentry_config.profiles_sample_rate,
    )

    meilisearch_client = providers.Resource(
        init_meilisearch,
        url=meilisearch_config.url,
        key=meilisearch_config.key,
    )
