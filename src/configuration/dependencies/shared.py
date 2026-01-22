from dependency_injector import containers, providers

from src.core.shared.infrastructure.services.email_sender import ConsoleEmailSender


class SharedContainer(containers.DeclarativeContainer):
    console_email_sender = providers.Singleton(ConsoleEmailSender)
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

