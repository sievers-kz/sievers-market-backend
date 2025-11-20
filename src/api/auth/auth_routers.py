from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.auth.auth_dto import (
    CreateUserDTO,
    EmailConfirmationDTO,
    LoginUserDTO,
    LoginResponseDTO,
    RefreshTokenDTO,
    ForgotPasswordDTO, ResetPasswordDTO,
)

from src.configuration.dependencies.depends import DependencyContainer
from src.core.auth.application.usecases import (
    CreateUserUseCase,
    EmailConfirmationUseCase,
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase
)

auth_router = APIRouter(prefix="/api/v1", tags=["Auth"])


@auth_router.post("/auth/registration")
@inject
async def create_user(
    user_data: CreateUserDTO,
    create_user_usecase: Annotated[
        CreateUserUseCase,
        Depends(
            Provide[
                DependencyContainer.create_user_usecase
            ]
        )
    ]
):
    await create_user_usecase.execute(user_data=user_data)
    return {"message": "Регистрация прошла успешно. Пожалуйста, подтвердите свою почту для завершения"}


@auth_router.post("/auth/email_confirmation")
@inject
async def confirm_email(
    confirmation_code: EmailConfirmationDTO,
    email_confirmation_usecase: Annotated[
        EmailConfirmationUseCase,
        Depends(
            Provide[
                DependencyContainer.email_confirmation_usecase
            ]
        )
    ]
):
    await email_confirmation_usecase.execute(confirmation_code)
    return {"message": "Ваша электронная почта успешно подтверждена!"}


@auth_router.post("/auth/login", response_model=LoginResponseDTO)
@inject
async def login_user(
    user_data: LoginUserDTO,
    login_user_usecase: Annotated[
        LoginUserUseCase,
        Depends(
            Provide[
                DependencyContainer.login_user_usecase
            ]
        )
    ]
):
    return await login_user_usecase.execute(user_data)


@auth_router.post("/auth/refresh", response_model=LoginResponseDTO)
@inject
async def refresh_token(
    token_data: RefreshTokenDTO,
    refresh_token_usecase: Annotated[
        RefreshTokenUseCase,
        Depends(
            Provide[
                DependencyContainer.refresh_token_usecase
            ]
        )
    ]
):
    return await refresh_token_usecase.execute(token_data)


@auth_router.post("/auth/logout")
@inject
async def logout_user(
    token_data: RefreshTokenDTO,
    logout_user_usecase: Annotated[
        LogoutUserUseCase,
        Depends(
            Provide[
                DependencyContainer.logout_user_usecase
            ]
        )
    ]
):
    await logout_user_usecase.execute(token_data)
    return {"message": "Вы вышли из системы"}


@auth_router.post("/auth/forgot-password")
@inject
async def request_forgot_password(
    forgot_password_dto: ForgotPasswordDTO,
    forgot_password_usecase: Annotated[
        ForgotPasswordUseCase,
        Depends(
            Provide[
                DependencyContainer.forgot_password_usecase
            ]
        )
    ]
):
    await forgot_password_usecase.execute(forgot_password_dto)
    return {"message": "Если указанная вами почта существует, мы отправили письмо с подтверждением"}


@auth_router.post("/auth/reset-password")
@inject
async def reset_user_password(
    reset_password_dto: ResetPasswordDTO,
    reset_password_usecase: Annotated[
        ResetPasswordUseCase,
        Depends(
            Provide[
                DependencyContainer.reset_password_usecase
            ]
        )
    ]
):
    await reset_password_usecase.execute(reset_password_dto)
    return {"message": "Пароль успешно изменён! Пожалуйста, войдите систему с новым паролем."}