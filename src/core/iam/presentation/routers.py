from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException, Response, status
from fastapi.params import Cookie, Security

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
from src.core.iam.presentation.dto import (
    AccountConfirmation,
    ChangeEmailRequest,
    ChangePasswordData,
    ConfirmEmailChangeRequest,
    CreateAccountRequest,
    ForgotPasswordData,
    LoginAccount,
    LoginResponse,
    RefreshData,
    ResendCodeRequest,
    ResetPasswordData,
)
from src.core.shared.infrastructure.services.api_session_service import (
    APISessionService,
)
from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user

iam = APIRouter(prefix="/api/v1/iam", tags=["IAM"])


@iam.post("/registration")
@inject
async def create_new_user(
    dto: CreateAccountRequest,
    usecase: Annotated[
        CreateAccountUseCase,
        Depends(Provide[ApplicationContainer.iam.create_account_usecase]),
    ],
):
    response = await usecase.execute(dto)
    return {
        "response": response,
        "message": "Регистрация успешно пройдена. "
        "Пожалуйста, подтвердите свою почту для завершения",
    }


@iam.post("/account_confirmation", response_model=LoginResponse | dict)
@inject
async def confirm_email(
    response: Response,
    dto: AccountConfirmation,
    usecase: Annotated[
        AccountConfirmationUseCase,
        Depends(Provide[ApplicationContainer.iam.account_confirmation_usecase]),
    ],
    api_session_service: Annotated[
        APISessionService,
        Depends(Provide[ApplicationContainer.shared.api_session_service]),
    ],
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = "web",
):
    tokens = await usecase.execute(dto)
    return api_session_service.prepare_response(response, tokens, client_type)


@iam.post("/resend-code")
@inject
async def resend_confirmation_code(
    dto: ResendCodeRequest,
    usecase: Annotated[
        ResendConfirmationCodeUseCase,
        Depends(Provide[ApplicationContainer.iam.resend_confirmation_code_usecase]),
    ],
):
    await usecase.execute(dto)
    return {
        "message": "Код подтверждения отправлен на указанный адрес электронной почты"
    }


@iam.post("/login", response_model=LoginResponse | dict)
@inject
async def login_user(
    response: Response,
    dto: LoginAccount,
    usecase: Annotated[
        LoginUserUseCase, Depends(Provide[ApplicationContainer.iam.login_user_usecase])
    ],
    api_session_service: Annotated[
        APISessionService,
        Depends(Provide[ApplicationContainer.shared.api_session_service]),
    ],
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = "web",
):
    tokens = await usecase.execute(dto)
    return api_session_service.prepare_response(response, tokens, client_type)


@iam.post("/refresh", response_model=LoginResponse | dict)
@inject
async def refresh_token(
    response: Response,
    usecase: Annotated[
        RefreshTokenUseCase,
        Depends(Provide[ApplicationContainer.iam.refresh_token_usecase]),
    ],
    api_session_service: Annotated[
        APISessionService,
        Depends(Provide[ApplicationContainer.shared.api_session_service]),
    ],
    dto: RefreshData | None = None,
    refresh_token_from_cookie: Annotated[
        str | None, Cookie(alias="refresh_token")
    ] = None,
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = "web",
):
    raw_refresh_token = refresh_token_from_cookie or (
        dto.refresh_token if dto else None
    )
    if not raw_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Рефреш-токен не найден в запросе",
        )

    refresh_dto = RefreshData(refresh_token=raw_refresh_token)
    new_tokens: LoginResponse = await usecase.execute(refresh_dto)

    return api_session_service.prepare_response(response, new_tokens, client_type)


@iam.post("/logout")
@inject
async def logout_user(
    response: Response,
    usecase: Annotated[
        LogoutUserUseCase,
        Depends(Provide[ApplicationContainer.iam.logout_user_usecase]),
    ],
    api_session_service: Annotated[
        APISessionService,
        Depends(Provide[ApplicationContainer.shared.api_session_service]),
    ],
    dto: RefreshData | None = None,
    refresh_token_from_cookie: Annotated[
        str | None, Cookie(alias="refresh_token")
    ] = None,
):
    raw_refresh_token = refresh_token_from_cookie or (
        dto.refresh_token if dto else None
    )

    if raw_refresh_token:
        logout_dto = RefreshData(refresh_token=raw_refresh_token)
        await usecase.execute(logout_dto)

    api_session_service.clear_session(response)
    return {"message": "Вы вышли из системы"}


@iam.post("/forgot-password")
@inject
async def request_forgot_password(
    dto: ForgotPasswordData,
    usecase: Annotated[
        ForgotPasswordUseCase,
        Depends(Provide[ApplicationContainer.iam.forgot_password_usecase]),
    ],
):
    await usecase.execute(dto)
    return {
        "message": "Если указанная вами почта существует, "
        "мы отправили письмо с подтверждением"
    }


@iam.post("/reset-password")
@inject
async def reset_user_password(
    dto: ResetPasswordData,
    usecase: Annotated[
        ResetPasswordUseCase,
        Depends(Provide[ApplicationContainer.iam.reset_password_usecase]),
    ],
):
    await usecase.execute(dto)
    return {
        "message": "Пароль успешно изменён! Пожалуйста, "
        "войдите систему с новым паролем."
    }


@iam.post("/change-password")
@inject
async def change_password(
    dto: ChangePasswordData,
    usecase: Annotated[
        ChangePasswordUseCase,
        Depends(Provide[ApplicationContainer.iam.change_password_usecase]),
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {
        "message": "Пароль успешно изменён! Пожалуйста, "
        "войдите систему с новым паролем."
    }


@iam.patch("/email/change")
@inject
async def request_email_change(
    dto: ChangeEmailRequest,
    usecase: Annotated[
        RequestEmailChangeUseCase,
        Depends(Provide[ApplicationContainer.iam.request_email_change_usecase]),
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {
        "message": "Мы отправили код на вашу почту. "
        "Подтвердите вашу новую электронную почту"
    }


@iam.patch("/email/confirm")
@inject
async def confirm_email_change(
    dto: ConfirmEmailChangeRequest,
    usecase: Annotated[
        ConfirmEmailChangeUseCase,
        Depends(Provide[ApplicationContainer.iam.confirm_email_change_usecase]),
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваша электронная почта успешно подтверждена!"}
