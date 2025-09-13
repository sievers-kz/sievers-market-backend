from datetime import timedelta

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.users.application.usecases import RegisterUserUseCase, LoginUserUseCase
from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.users.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.users.infrastructure.user_unit_of_work import UserUnitOfWork


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

    unit_of_work = providers.Factory(
        UserUnitOfWork,
        session_factory=async_session_maker
    )
    password_hasher = providers.Singleton(BcryptPasswordHasher)

    register_usecase = providers.Factory(
        RegisterUserUseCase,
        unit_of_work=unit_of_work,
        hasher=password_hasher
    )

    token_service = providers.Singleton(
        PyJWTTokenService,
        secret_key=config.SECRET_KEY,
        algorithm=config.ALGORITHM,

        access_token_lifetime=providers.Factory(
            timedelta,
            minutes=config.ACCESS_TOKEN_LIFETIME.as_int()
        ),
        refresh_token_lifetime=providers.Factory(
            timedelta,
            days=config.REFRESH_TOKEN_LIFETIME.as_int()
        ),
        email_token_lifetime=providers.Factory(
            timedelta,
            hours=config.EMAIL_TOKEN_LIFETIME.as_int()
        )
    )

    login_usecase = providers.Factory(
        LoginUserUseCase,
        unit_of_work=unit_of_work,
        token_service=token_service,
    )
