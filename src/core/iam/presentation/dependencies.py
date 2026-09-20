from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.iam.application.usecases import (
    AccountConfirmationUseCase,
    ChangePasswordUseCase,
    ConfirmEmailChangeUseCase,
    CreateAccountUseCase,
    ForgotPasswordUseCase,
    LoginUserUseCase,
    LogoutUserUseCase,
    RefreshTokenUseCase,
    RequestEmailChangeUseCase,
    ResendConfirmationCodeUseCase,
    ResetPasswordUseCase,
)
from src.core.iam.infrastructure.services.query_service import GetMeQueryService
from src.core.shared.infrastructure.services.api_session_service import (
    APISessionService,
)

APISessionServiceDependency = Annotated[
    APISessionService,
    Depends(Provide[ApplicationContainer.shared.api_session_service]),
]

GetMeQueryServiceDependency = Annotated[GetMeQueryService, Depends(Provide[ApplicationContainer.iam.query_service])]

CreateAccountUseCaseDependency = Annotated[
    CreateAccountUseCase,
    Depends(Provide[ApplicationContainer.iam.create_account_usecase]),
]

AccountConfirmationUseCaseDependency = Annotated[
    AccountConfirmationUseCase,
    Depends(Provide[ApplicationContainer.iam.account_confirmation_usecase]),
]

ResendConfirmationCodeUseCaseDependency = Annotated[
    ResendConfirmationCodeUseCase,
    Depends(Provide[ApplicationContainer.iam.resend_confirmation_code_usecase]),
]

LoginUserUseCaseDependency = Annotated[LoginUserUseCase, Depends(Provide[ApplicationContainer.iam.login_user_usecase])]

RefreshTokenUseCaseDependency = Annotated[
    RefreshTokenUseCase,
    Depends(Provide[ApplicationContainer.iam.refresh_token_usecase]),
]

LogoutUserUseCaseDependency = Annotated[
    LogoutUserUseCase,
    Depends(Provide[ApplicationContainer.iam.logout_user_usecase]),
]

ForgotPasswordUseCaseDependency = Annotated[
    ForgotPasswordUseCase,
    Depends(Provide[ApplicationContainer.iam.forgot_password_usecase]),
]

ResetPasswordUseCaseDependency = Annotated[
    ResetPasswordUseCase,
    Depends(Provide[ApplicationContainer.iam.reset_password_usecase]),
]

ChangePasswordUseCaseDependency = Annotated[
    ChangePasswordUseCase,
    Depends(Provide[ApplicationContainer.iam.change_password_usecase]),
]

RequestEmailChangeUseCaseDependency = Annotated[
    RequestEmailChangeUseCase,
    Depends(Provide[ApplicationContainer.iam.request_email_change_usecase]),
]

ConfirmEmailChangeUseCaseDependency = Annotated[
    ConfirmEmailChangeUseCase,
    Depends(Provide[ApplicationContainer.iam.confirm_email_change_usecase]),
]
