from dependency_injector import containers, providers

from src.configuration.settings.settings import ApplicationSettings


class ConfigurationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration(pydantic_settings=[ApplicationSettings()])
    database = configuration.database
    authentication = configuration.authentication
    sendgrid = configuration.sendgrid
    object_storage = configuration.object_storage
    redis = configuration.redis_config
    resend_config = configuration.resend_config
