from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.params import Security

from src.core.iam.presentation.dto import (
    AccountConfirmation,
    LoginResponse,
    RefreshData,
    ForgotPasswordData,
    ResetPasswordData,
    ChangePasswordData,
    LoginAccount,
    ResendCodeRequest,
    CreateUserRequest,
    ChangeEmailRequest,
    ConfirmEmailChangeRequest,
    ConfirmPhoneChangeRequest,
    ChangePhoneRequest,
)

from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user

from src.configuration.dependencies.container import ApplicationContainer

from src.core.iam.application.usecases import (
    AccountConfirmationUseCase,
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase,
    ChangePasswordUseCase,
    ResendConfirmationCodeUseCase,
    CreateAccountUseCase,
    ConfirmEmailChangeUseCase,
    RequestEmailChangeUseCase,
    ConfirmPhoneChangeUseCase,
    RequestPhoneChangeUseCase
)


iam = APIRouter(prefix="/api/v1/iam", tags=["IAM"])


@iam.post("/registration")
@inject
async def create_new_user(
    dto: CreateUserRequest,
    usecase: Annotated[
        CreateAccountUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.create_account_usecase
            ]
        )
    ]
):
    response = await usecase.execute(dto)
    return {
        "response": response,
        "message": "Регистрация успешно пройдена. Пожалуйста, подтвердите свою почту для завершения"
    }


@iam.post("/account_confirmation")
@inject
async def confirm_email(
    dto: AccountConfirmation,
    usecase: Annotated[
        AccountConfirmationUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.account_confirmation_usecase
            ]
        )
    ]
):
    response = await usecase.execute(dto)
    return {
        "message": "Ваша электронная почта успешно подтверждена!",
        "response": response,
    }


@iam.post("/resend-code")
@inject
async def resend_confirmation_code(
    dto: ResendCodeRequest,
    usecase: Annotated[
        ResendConfirmationCodeUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.resend_confirmation_code_usecase
            ]
        )
    ]
):
    await usecase.execute(dto)
    return {"message": "Код подтверждения отправлен на указанный адрес электронной почты"}


@iam.post("/login")
@inject
async def login_user(
    dto: LoginAccount,
    usecase: Annotated[
        LoginUserUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.login_user_usecase
            ]
        )
    ]
):
    return await usecase.execute(dto)


@iam.post("/refresh", response_model=LoginResponse)
@inject
async def refresh_token(
    dto: RefreshData,
    usecase: Annotated[
        RefreshTokenUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.refresh_token_usecase
            ]
        )
    ]
):
    return await usecase.execute(dto)


@iam.post("/logout")
@inject
async def logout_user(
    dto: RefreshData,
    usecase: Annotated[
        LogoutUserUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.logout_user_usecase
            ]
        )
    ]
):
    await usecase.execute(dto)
    return {"message": "Вы вышли из системы"}


@iam.post("/forgot-password")
@inject
async def request_forgot_password(
    dto: ForgotPasswordData,
    usecase: Annotated[
        ForgotPasswordUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.forgot_password_usecase
            ]
        )
    ]
):
    await usecase.execute(dto)
    return {"message": "Если указанная вами почта существует, мы отправили письмо с подтверждением"}


@iam.post("/reset-password")
@inject
async def reset_user_password(
    dto: ResetPasswordData,
    usecase: Annotated[
        ResetPasswordUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.reset_password_usecase
            ]
        )
    ]
):
    await usecase.execute(dto)
    return {"message": "Пароль успешно изменён! Пожалуйста, войдите систему с новым паролем."}


@iam.post("/change-password")
@inject
async def change_password(
    dto: ChangePasswordData,
    usecase: Annotated[
        ChangePasswordUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.change_password_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Пароль успешно изменён! Пожалуйста, войдите систему с новым паролем."}


@iam.patch("/email/change")
@inject
async def request_email_change(
    dto: ChangeEmailRequest,
    usecase: Annotated[
        RequestEmailChangeUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.request_email_change_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Мы отправили код на вашу почту. Подтвердите вашу новую электронную почту"}


@iam.patch("/email/confirm")
@inject
async def confirm_email_change(
    dto: ConfirmEmailChangeRequest,
    usecase: Annotated[
        ConfirmEmailChangeUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.confirm_email_change_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваша электронная почта успешно подтверждена!"}


@iam.post("/phone/change")
@inject
async def request_change_phone(
    dto: ChangePhoneRequest,
    usecase: Annotated[
        RequestPhoneChangeUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.request_phone_change_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Мы отправили письмо подтверждения на вашу электронную почту"}


@iam.patch("/phone/confirm")
@inject
async def confirm_change_phone(
    dto: ConfirmPhoneChangeRequest,
    usecase: Annotated[
        ConfirmPhoneChangeUseCase,
        Depends(
            Provide[
                ApplicationContainer.iam.confirm_phone_change_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваш номер телефона успешно изменен!"}
