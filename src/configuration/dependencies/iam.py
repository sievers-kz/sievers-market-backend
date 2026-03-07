from datetime import timedelta

from dependency_injector import containers, providers

from src.core.iam.application.usecases import (
    CreateUserUseCase,
    AccountConfirmationUseCase,
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase,
    ChangePasswordUseCase, ResendConfirmationCodeUseCase
)
from src.core.iam.infrastructure.adapters.account_confirmation import EmailNotifierAdapter
from src.core.iam.infrastructure.adapters.profile_creator import ProfileCreatorAdapter

from src.core.iam.infrastructure.iam_unit_of_work import IAMUnitOfWork
from src.core.iam.infrastructure.factory import AccountFactory
from src.core.iam.infrastructure.repository import AccountRepository

from src.core.iam.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.shared.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer


class IAMContainer(containers.DeclarativeContainer):
    auth_config = providers.Configuration()
    database_session = providers.Dependency()
    customer_service = providers.Dependency()

    console_email_sender = providers.Dependency()
    email_confirmation_template = providers.Dependency()
    password_recovery_template = providers.Dependency()

    account_repository = providers.Factory(
        AccountRepository,
        session=database_session
    )

    iam_unit_of_work = providers.Factory(
        IAMUnitOfWork,
        session=database_session
    )

    bcrypt_password_hasher = providers.Singleton(BcryptPasswordHasher)
    phonenumber_normalizer = providers.Singleton(PhoneNormalizer)

    account_factory = providers.Factory(
        AccountFactory,
        phone_normalizer=phonenumber_normalizer,
        password_hasher=bcrypt_password_hasher
    )

    pyjwt_token_service = providers.Singleton(
        PyJWTTokenService,
        secret_key=auth_config.secret_key,
        algorithm=auth_config.algorithm,

        access_token_lifetime=providers.Factory(
            timedelta,
            minutes=auth_config.access_token_lifetime.as_int()
        ),
        refresh_token_lifetime=providers.Factory(
            timedelta,
            days=auth_config.refresh_token_lifetime.as_int()
        ),
        email_token_lifetime=providers.Factory(
            timedelta,
            hours=auth_config.email_token_lifetime.as_int()
        ),
        password_reset_token_lifetime=providers.Factory(
            timedelta,
            hours=auth_config.password_reset_token_lifetime.as_int()
        )
    )

    profile_creator_adapter = providers.Factory(
        ProfileCreatorAdapter,
        customer_service=customer_service,
    )

    email_notifier_adapter = providers.Factory(
        EmailNotifierAdapter,
        sender=console_email_sender,
        email_confirmation_template=email_confirmation_template,
        password_recovery_template=password_recovery_template
    )

    create_user_usecase = providers.Factory(
        CreateUserUseCase,
        unit_of_work=iam_unit_of_work,
        token_service=pyjwt_token_service,
        factory=account_factory,
        profile_creator=profile_creator_adapter,
        notifier=email_notifier_adapter
    )

    account_confirmation_usecase = providers.Factory(
        AccountConfirmationUseCase,
        unit_of_work=iam_unit_of_work
    )

    resend_confirmation_code_usecase = providers.Factory(
        ResendConfirmationCodeUseCase,
        unit_of_work=iam_unit_of_work,
        token_service=pyjwt_token_service,
        notifier=email_notifier_adapter
    )

    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        unit_of_work=iam_unit_of_work,
        token_service=pyjwt_token_service,
        password_hasher=bcrypt_password_hasher
    )

    refresh_token_usecase = providers.Factory(
        RefreshTokenUseCase,
        unit_of_work=iam_unit_of_work,
        token_service=pyjwt_token_service
    )

    logout_user_usecase = providers.Factory(
        LogoutUserUseCase,
        unit_of_work=iam_unit_of_work,
    )

    forgot_password_usecase = providers.Factory(
        ForgotPasswordUseCase,
        unit_of_work=iam_unit_of_work,
        token_service=pyjwt_token_service,
        notifier=email_notifier_adapter
    )

    reset_password_usecase = providers.Factory(
        ResetPasswordUseCase,
        unit_of_work=iam_unit_of_work,
        token_service=pyjwt_token_service,
        password_hasher=bcrypt_password_hasher
    )

    change_password_usecase = providers.Factory(
        ChangePasswordUseCase,
        unit_of_work=iam_unit_of_work,
        password_hasher=bcrypt_password_hasher
    )
