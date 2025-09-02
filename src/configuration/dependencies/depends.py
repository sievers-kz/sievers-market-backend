import uuid

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.configuration.conf.settings import DatabaseConnectionSettings
from src.configuration.database.connection import get_async_session
from src.core.users.application.usecases import RegisterUserUseCase
from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.users.infrastructure.user_repository import UserRepository


class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.users.user_routers"
        ]
    )

    config = providers.Configuration()

    async_engine = providers.Singleton(
        create_async_engine,
        url=config.database_url,
        echo=True
    )

    async_session_maker = providers.Singleton(
        sessionmaker,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async_session = providers.Resource(
        get_async_session,
        session_maker=async_session_maker
    )

    user_repository = providers.Factory(
        UserRepository,
        session=async_session
    )

    password_hasher = providers.Singleton(BcryptPasswordHasher)

    register_usecase = providers.Factory(
        RegisterUserUseCase,
        user_repo=user_repository,
        hasher=password_hasher
    )


