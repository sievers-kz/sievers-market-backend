from datetime import timedelta

from dependency_injector import containers, providers

from src.core.shared.infrastructure.services.api_session_service import (
    APISessionService,
)
from src.core.shared.infrastructure.services.arq_service import ArqService
from src.core.shared.infrastructure.services.email_sender import (
    ConsoleEmailSender,
    ResendEmailSender,
)
from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer
from src.core.shared.infrastructure.services.redis_service import RedisService


class SharedContainer(containers.DeclarativeContainer):
    resend_config = providers.Configuration()
    application_settings = providers.Configuration()

    console_email_sender = providers.Singleton(ConsoleEmailSender)
    phone_normalizer = providers.Singleton(PhoneNormalizer)

    resend_sender = providers.Singleton(
        ResendEmailSender,
        api_key=resend_config.api_key,
        from_email=resend_config.from_email,
    )

    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    redis_client = providers.Dependency()
    redis_service = providers.Singleton(RedisService, client=redis_client)

    arq_pool = providers.Dependency()
    arq_service = providers.Singleton(ArqService, pool=arq_pool)

    api_session_service = providers.Factory(
        APISessionService,
        mode=application_settings.mode,
        access_token_lifetime=providers.Factory(
            timedelta,
            minutes=application_settings.authentication.access_token_lifetime.as_int(),
        ),
        refresh_token_lifetime=providers.Factory(
            timedelta,
            days=application_settings.authentication.refresh_token_lifetime.as_int(),
        ),
    )
