from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.configuration.database.connection import get_database_session
from src.core.shared.infrastructure.services.email_sender import SendGridEmailSender


class GatewaysContainer(containers.DeclarativeContainer):
    database_config = providers.Configuration()
    sendgrid_config = providers.Configuration()

    buyer_repository = providers.Dependency()
    seller_repository = providers.Dependency()

    async_engine = providers.Singleton(
        create_async_engine,
        url=database_config.database_url
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=async_engine,
        expire_on_commit=False,
        autoflush=False
    )

    database_session = providers.Resource(
        get_database_session,
        session_factory=session_factory
    )

    sendgrid_sender = providers.Singleton(
        SendGridEmailSender,
        api_key=sendgrid_config.api_key,
        from_email=sendgrid_config.from_email,
    )

