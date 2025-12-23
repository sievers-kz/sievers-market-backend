from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.shared.infrastructure.services.email_sender import SendGridEmailSender


class GatewaysContainer(containers.DeclarativeContainer):
    database_config = providers.Dependency()
    sendgrid_config = providers.Dependency()

    async_engine = providers.Singleton(
        create_async_engine,
        url=database_config.provided["database_url"],
        echo=True
    )

    session_factory = providers.Singleton(
        sessionmaker,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    sendgrid_sender = providers.Singleton(
        SendGridEmailSender,
        api_key=sendgrid_config.provided["api_key"],
        from_email=sendgrid_config.provided["from_email"],
        email_confirmation_template_id=sendgrid_config.provided["email_confirmation_template_id"],
        password_reset_template_id=sendgrid_config.provided["password_reset_template_id"]
    )
