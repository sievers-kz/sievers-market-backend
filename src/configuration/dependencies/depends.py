from datetime import timedelta

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.auth.application.usecases import (
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase
)

from src.core.users.application.usecases import (
    CreateUserUseCase,
    EmailConfirmationUseCase,
    ResetPasswordUseCase
)

from src.core.auth.infrastructure.auth_unit_of_work import AuthUnitOfWork

from src.core.shared.infrastructure.services.email_sender import ConsoleEmailSender, SendGridEmailSender
from src.core.shared.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.shared.infrastructure.composite_uow import UserIdentityUnitOfWork
from src.core.users.infrastructure.user_unit_of_work import UserUnitOfWork


class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.users.user_routers",
            "src.api.auth.auth_routers"
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
        expire_on_commit=False,
        autoflush=False
    )

    user_unit_of_work = providers.Factory(
        UserUnitOfWork,
        session_factory=async_session_maker
    )
    identity_unit_of_work = providers.Factory(
        AuthUnitOfWork,
        session_factory=async_session_maker
    )

    user_identity_unit_of_work = providers.Factory(
        UserIdentityUnitOfWork,
        session_factory=async_session_maker
    )

    password_hasher = providers.Singleton(BcryptPasswordHasher)
    console_email_sender = providers.Singleton(ConsoleEmailSender)

    sendgrid_email_sender = providers.Singleton(
        SendGridEmailSender,
        api_key=config.SEND_GRID_API_KEY,
        from_email=config.FROM_EMAIL,
        email_confirmation_template_id=config.EMAIL_CONFIRMATION_TEMPLATE_ID,
        password_reset_template_id=config.PASSWORD_RESET_TEMPLATE_ID
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
        ),
        password_reset_token_lifetime=providers.Factory(
            timedelta,
            hours=config.PASSWORD_RESET_TOKEN_LIFETIME.as_int()
        )
    )

    create_user_usecase = providers.Factory(
        CreateUserUseCase,
        unit_of_work=user_identity_unit_of_work,
        email_sender=console_email_sender,
        token_service=token_service
    )

    email_confirmation_usecase = providers.Factory(
        EmailConfirmationUseCase,
        unit_of_work=user_identity_unit_of_work
    )

    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=token_service,
        password_hasher=password_hasher
    )

    refresh_token_usecase = providers.Factory(
        RefreshTokenUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=token_service
    )

    logout_user_usecase = providers.Factory(
        LogoutUserUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=token_service
    )

    forgot_password_usecase = providers.Factory(
        ForgotPasswordUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=token_service,
        email_sender=console_email_sender
    )

    reset_password_usecase = providers.Factory(
        ResetPasswordUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=token_service,
        password_hasher=password_hasher
    )
