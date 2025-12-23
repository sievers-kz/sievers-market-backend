from datetime import timedelta

from dependency_injector import containers, providers

from src.core.auth.application.usecases import (
    CreateUserUseCase,
    EmailConfirmationUseCase,
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase
)

from src.core.auth.infrastructure.auth_unit_of_work import AuthUnitOfWork
from src.core.users.infrastructure.user_unit_of_work import UserUnitOfWork
from src.core.shared.infrastructure.composite_uow import UserIdentityUnitOfWork

from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.shared.infrastructure.services.email_sender import ConsoleEmailSender
from src.core.shared.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer

from src.core.users.application.usecases import (
    ChangeFullnameUseCase,
    ChangeEmailUseCase,
    ChangePhoneUseCase,
    ChangeOrganizationFullnameUseCase,
    ChangeDocumentValueUseCase,
    ChangeAvatarURLUsecase,
    ChangePasswordUseCase
)


class IAMContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.users.user_routers",
            "src.api.auth.auth_routers"
        ]
    )

    auth_config = providers.Dependency()
    session_factory = providers.Dependency()
    sendgrid_sender = providers.Dependency()

    user_unit_of_work = providers.Factory(
        UserUnitOfWork,
        session_factory=session_factory
    )                                    # TODO: Restructure UserUoW & IdentityUoW & UserIdentityUoW to IAMUnitOfWork
    identity_unit_of_work = providers.Factory(
        AuthUnitOfWork,
        session_factory=session_factory
    )
    user_identity_unit_of_work = providers.Factory(
        UserIdentityUnitOfWork,
        session_factory=session_factory
    )

    bcrypt_password_hasher = providers.Singleton(BcryptPasswordHasher)
    console_email_sender = providers.Singleton(ConsoleEmailSender)
    phonenumber_normalizer = providers.Singleton(PhoneNormalizer)

    pyjwt_token_service = providers.Singleton(
        PyJWTTokenService,
        secret_key=auth_config.provided["secret_key"],
        algorithm=auth_config.provided["algorithm"],

        access_token_lifetime=providers.Factory(
            timedelta,
            minutes=auth_config.provided["access_token_lifetime"]
        ),
        refresh_token_lifetime=providers.Factory(
            timedelta,
            days=auth_config.provided["refresh_token_lifetime"]
        ),
        email_token_lifetime=providers.Factory(
            timedelta,
            hours=auth_config.provided["email_token_lifetime"]
        ),
        password_reset_token_lifetime=providers.Factory(
            timedelta,
            hours=auth_config.provided["password_reset_token_lifetime"]
        )
    )

    create_user_usecase = providers.Factory(
        CreateUserUseCase,
        unit_of_work=user_identity_unit_of_work,
        email_sender=console_email_sender,
        token_service=pyjwt_token_service
    )

    email_confirmation_usecase = providers.Factory(
        EmailConfirmationUseCase,
        unit_of_work=user_identity_unit_of_work
    )

    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=pyjwt_token_service,
        password_hasher=bcrypt_password_hasher
    )

    refresh_token_usecase = providers.Factory(
        RefreshTokenUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=pyjwt_token_service
    )

    logout_user_usecase = providers.Factory(
        LogoutUserUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=pyjwt_token_service
    )

    forgot_password_usecase = providers.Factory(
        ForgotPasswordUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=pyjwt_token_service,
        email_sender=console_email_sender
    )

    reset_password_usecase = providers.Factory(
        ResetPasswordUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=pyjwt_token_service,
        password_hasher=bcrypt_password_hasher
    )

    change_fullname_usecase = providers.Factory(
        ChangeFullnameUseCase,
        unit_of_work=user_unit_of_work,
        token_service=pyjwt_token_service
    )

    change_email_usecase = providers.Factory(
        ChangeEmailUseCase,
        unit_of_work=user_unit_of_work,
        token_service=pyjwt_token_service
    )

    change_phone_usecase = providers.Factory(
        ChangePhoneUseCase,
        unit_of_work=user_unit_of_work,
        token_service=pyjwt_token_service,
        phone_normalizer=phonenumber_normalizer
    )

    change_organization_fullname_usecase = providers.Factory(
        ChangeOrganizationFullnameUseCase,
        unit_of_work=user_unit_of_work,
        token_service=pyjwt_token_service,
    )

    change_document_value_usecase = providers.Factory(
        ChangeDocumentValueUseCase,
        unit_of_work=user_unit_of_work,
        token_service=pyjwt_token_service,
    )

    change_avatar_url_usecase = providers.Factory(
        ChangeAvatarURLUsecase,
        unit_of_work=user_unit_of_work,
        token_service=pyjwt_token_service
    )

    change_password_usecase = providers.Factory(
        ChangePasswordUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=pyjwt_token_service,
        password_hasher=bcrypt_password_hasher
    )
