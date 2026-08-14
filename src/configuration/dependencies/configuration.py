from dependency_injector import containers, providers

from src.configuration.settings.settings import ApplicationSettings


class ConfigurationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration(pydantic_settings=[ApplicationSettings()])
    database = configuration.database
    authentication = configuration.authentication
    sendgrid = configuration.sendgrid
    minio_config = configuration.minio_config
    redis = configuration.redis_config
    resend_config = configuration.resend_config
    sentry_config = configuration.sentry_config
    kgd_settings = configuration.kgd_settings
    meilisearch_config = configuration.meilisearch_config
