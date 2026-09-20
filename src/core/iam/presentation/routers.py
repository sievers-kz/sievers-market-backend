from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, Header, Response
from fastapi.params import Cookie, Security

from src.core.iam.domain.exceptions import RefreshTokenMissingError
from src.core.iam.presentation.dependencies import (
    AccountConfirmationUseCaseDependency,
    APISessionServiceDependency,
    ChangePasswordUseCaseDependency,
    ConfirmEmailChangeUseCaseDependency,
    CreateAccountUseCaseDependency,
    ForgotPasswordUseCaseDependency,
    GetMeQueryServiceDependency,
    LoginUserUseCaseDependency,
    LogoutUserUseCaseDependency,
    RefreshTokenUseCaseDependency,
    RequestEmailChangeUseCaseDependency,
    ResendConfirmationCodeUseCaseDependency,
    ResetPasswordUseCaseDependency,
)
from src.core.iam.presentation.documentation import (
    CHANGE_PASSWORD_DOC,
    CONFIRM_ACCOUNT_DOC,
    CONFIRM_EMAIL_CHANGE_DOC,
    CREATE_NEW_USER_DOC,
    GET_ME_DOC,
    LOGIN_USER_DOC,
    LOGOUT_USER_DOC,
    REFRESH_TOKEN_DOC,
    REQUEST_EMAIL_CHANGE_DOC,
    REQUEST_FORGOT_PASSWORD_DOC,
    RESEND_CONFIRMATION_CODE_DOC,
    RESET_USER_PASSWORD_DOC,
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
    MeResponse,
    RefreshData,
    ResendCodeRequest,
    ResetPasswordData,
)
from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user

iam = APIRouter(prefix="/api/v1/iam", tags=["IAM"])


@iam.get(
    "/me",
    response_model=MeResponse,
    operation_id=GET_ME_DOC.operation_id,
    summary=GET_ME_DOC.summary,
    responses=GET_ME_DOC.responses_doc,
    description=GET_ME_DOC.description,
)
@inject
async def get_me(
    service: GetMeQueryServiceDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    return await service.get_me(current_user.id)


@iam.post(
    "/",
    operation_id=CREATE_NEW_USER_DOC.operation_id,
    summary=CREATE_NEW_USER_DOC.summary,
    responses=CREATE_NEW_USER_DOC.responses_doc,
    description=CREATE_NEW_USER_DOC.description,
)
@inject
async def create_new_user(
    dto: CreateAccountRequest,
    usecase: CreateAccountUseCaseDependency,
):
    response = await usecase.execute(dto)
    return {
        "response": response,
        "message": "Регистрация успешно пройдена. " "Пожалуйста, подтвердите свою почту для завершения",
    }


@iam.post(
    "/account/confirm",
    response_model=LoginResponse | dict,
    operation_id=CONFIRM_ACCOUNT_DOC.operation_id,
    summary=CONFIRM_ACCOUNT_DOC.summary,
    responses=CONFIRM_ACCOUNT_DOC.responses_doc,
    description=CONFIRM_ACCOUNT_DOC.description,
)
@inject
async def confirm_account(
    response: Response,
    dto: AccountConfirmation,
    usecase: AccountConfirmationUseCaseDependency,
    api_session_service: APISessionServiceDependency,
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = "web",
):
    tokens = await usecase.execute(dto)
    return api_session_service.prepare_response(response, tokens, client_type)


@iam.post(
    "/code/resend",
    operation_id=RESEND_CONFIRMATION_CODE_DOC.operation_id,
    summary=RESEND_CONFIRMATION_CODE_DOC.summary,
    responses=RESEND_CONFIRMATION_CODE_DOC.responses_doc,
    description=RESEND_CONFIRMATION_CODE_DOC.description,
)
@inject
async def resend_confirmation_code(
    dto: ResendCodeRequest,
    usecase: ResendConfirmationCodeUseCaseDependency,
):
    await usecase.execute(dto)
    return {"message": "Код подтверждения отправлен на указанный адрес электронной почты"}


@iam.post(
    "/login",
    response_model=LoginResponse | dict,
    operation_id=LOGIN_USER_DOC.operation_id,
    summary=LOGIN_USER_DOC.summary,
    responses=LOGIN_USER_DOC.responses_doc,
    description=LOGIN_USER_DOC.description,
)
@inject
async def login_user(
    response: Response,
    dto: LoginAccount,
    usecase: LoginUserUseCaseDependency,
    api_session_service: APISessionServiceDependency,
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = "web",
):
    tokens = await usecase.execute(dto)
    return api_session_service.prepare_response(response, tokens, client_type)


@iam.post(
    "/refresh",
    response_model=LoginResponse | dict,
    operation_id=REFRESH_TOKEN_DOC.operation_id,
    summary=REFRESH_TOKEN_DOC.summary,
    responses=REFRESH_TOKEN_DOC.responses_doc,
    description=REFRESH_TOKEN_DOC.description,
)
@inject
async def refresh_token(
    response: Response,
    usecase: RefreshTokenUseCaseDependency,
    api_session_service: APISessionServiceDependency,
    dto: RefreshData | None = None,
    refresh_token_from_cookie: Annotated[str | None, Cookie(alias="refresh_token")] = None,
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = "web",
):
    raw_refresh_token = refresh_token_from_cookie or (dto.refresh_token if dto else None)
    if not raw_refresh_token:
        raise RefreshTokenMissingError()

    refresh_dto = RefreshData(refresh_token=raw_refresh_token)
    new_tokens: LoginResponse = await usecase.execute(refresh_dto)

    return api_session_service.prepare_response(response, new_tokens, client_type)


@iam.post(
    "/logout",
    operation_id=LOGOUT_USER_DOC.operation_id,
    summary=LOGOUT_USER_DOC.summary,
    responses=LOGOUT_USER_DOC.responses_doc,
    description=LOGOUT_USER_DOC.description,
)
@inject
async def logout_user(
    response: Response,
    usecase: LogoutUserUseCaseDependency,
    api_session_service: APISessionServiceDependency,
    dto: RefreshData | None = None,
    refresh_token_from_cookie: Annotated[str | None, Cookie(alias="refresh_token")] = None,
):
    raw_refresh_token = refresh_token_from_cookie or (dto.refresh_token if dto else None)

    if raw_refresh_token:
        logout_dto = RefreshData(refresh_token=raw_refresh_token)
        await usecase.execute(logout_dto)

    api_session_service.clear_session(response)
    return {"message": "Вы вышли из системы"}


@iam.post(
    "/password/forgot",
    operation_id=REQUEST_FORGOT_PASSWORD_DOC.operation_id,
    summary=REQUEST_FORGOT_PASSWORD_DOC.summary,
    responses=REQUEST_FORGOT_PASSWORD_DOC.responses_doc,
    description=REQUEST_FORGOT_PASSWORD_DOC.description,
)
@inject
async def request_forgot_password(
    dto: ForgotPasswordData,
    usecase: ForgotPasswordUseCaseDependency,
):
    await usecase.execute(dto)
    return {"message": "Если указанная вами почта существует, " "мы отправили письмо с подтверждением"}


@iam.post(
    "/password/reset",
    operation_id=RESET_USER_PASSWORD_DOC.operation_id,
    summary=RESET_USER_PASSWORD_DOC.summary,
    responses=RESET_USER_PASSWORD_DOC.responses_doc,
    description=RESET_USER_PASSWORD_DOC.description,
)
@inject
async def reset_user_password(
    response: Response,
    dto: ResetPasswordData,
    api_session_service: APISessionServiceDependency,
    usecase: ResetPasswordUseCaseDependency,
):
    await usecase.execute(dto)
    api_session_service.clear_session(response)

    return {"message": "Пароль успешно изменён! Пожалуйста, " "войдите систему с новым паролем."}


@iam.post(
    "/password/change",
    operation_id=CHANGE_PASSWORD_DOC.operation_id,
    summary=CHANGE_PASSWORD_DOC.summary,
    responses=CHANGE_PASSWORD_DOC.responses_doc,
    description=CHANGE_PASSWORD_DOC.description,
)
@inject
async def change_password(
    respone: Response,
    dto: ChangePasswordData,
    usecase: ChangePasswordUseCaseDependency,
    api_session_service: APISessionServiceDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    api_session_service.clear_session(respone)

    return {"message": "Пароль успешно изменён! Пожалуйста, " "войдите систему с новым паролем."}


@iam.patch(
    "/email/change",
    operation_id=REQUEST_EMAIL_CHANGE_DOC.operation_id,
    summary=REQUEST_EMAIL_CHANGE_DOC.summary,
    responses=REQUEST_EMAIL_CHANGE_DOC.responses_doc,
    description=REQUEST_EMAIL_CHANGE_DOC.description,
)
@inject
async def request_email_change(
    dto: ChangeEmailRequest,
    usecase: RequestEmailChangeUseCaseDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Мы отправили код на вашу почту. " "Подтвердите вашу новую электронную почту"}


@iam.patch(
    "/email/confirm",
    operation_id=CONFIRM_EMAIL_CHANGE_DOC.operation_id,
    summary=CONFIRM_EMAIL_CHANGE_DOC.summary,
    responses=CONFIRM_EMAIL_CHANGE_DOC.responses_doc,
    description=CONFIRM_EMAIL_CHANGE_DOC.description,
)
@inject
async def confirm_email_change(
    dto: ConfirmEmailChangeRequest,
    usecase: ConfirmEmailChangeUseCaseDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваша электронная почта успешно подтверждена!"}
