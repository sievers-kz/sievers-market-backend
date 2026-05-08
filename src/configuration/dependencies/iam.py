from datetime import timedelta

from dependency_injector import containers, providers

from src.core.iam.application.services.otp import OTPService
from src.core.iam.application.usecases import (
    CreateUserUseCase,
    AccountConfirmationUseCase,
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase,
    ChangePasswordUseCase, ResendConfirmationCodeUseCase, RequestEmailChangeUseCase, ConfirmEmailChangeUseCase,
    RequestPhoneChangeUseCase, ConfirmPhoneChangeUseCase
)


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
    redis_service = providers.Dependency()
    arq_service = providers.Dependency()

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

    otp_service = providers.Factory(
        OTPService,
        cache=redis_service,
        queue=arq_service,
    )

    create_user_usecase = providers.Factory(
        CreateUserUseCase,
        unit_of_work=iam_unit_of_work,
        factory=account_factory,
        customer_service=customer_service,
        otp_service=otp_service
    )

    account_confirmation_usecase = providers.Factory(
        AccountConfirmationUseCase,
        unit_of_work=iam_unit_of_work,
        otp_service=otp_service,
    )

    resend_confirmation_code_usecase = providers.Factory(
        ResendConfirmationCodeUseCase,
        unit_of_work=iam_unit_of_work,
        otp_service=otp_service,
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
        otp_service=otp_service,
    )

    reset_password_usecase = providers.Factory(
        ResetPasswordUseCase,
        unit_of_work=iam_unit_of_work,
        password_hasher=bcrypt_password_hasher,
        otp_service=otp_service,
    )

    change_password_usecase = providers.Factory(
        ChangePasswordUseCase,
        unit_of_work=iam_unit_of_work,
        password_hasher=bcrypt_password_hasher
    )

    request_email_change_usecase = providers.Factory(
        RequestEmailChangeUseCase,
        uow=iam_unit_of_work,
        otp_service=otp_service,
        cache_service=redis_service,
    )

    confirm_email_change_usecase = providers.Factory(
        ConfirmEmailChangeUseCase,
        uow=iam_unit_of_work,
        otp_service=otp_service,
        cache_service=redis_service,
    )

    request_phone_change_usecase = providers.Factory(
        RequestPhoneChangeUseCase,
        uow=iam_unit_of_work,
        otp_service=otp_service,
        cache_service=redis_service,
    )

    confirm_phone_change_usecase = providers.Factory(
        ConfirmPhoneChangeUseCase,
        uow=iam_unit_of_work,
        otp_service=otp_service,
        cache_service=redis_service,
    )
