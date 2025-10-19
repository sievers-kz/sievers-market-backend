from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.auth.auth_dto import LoginUserDTO, LoginResponseDTO, RefreshTokenDTO, ForgotPasswordDTO
from src.configuration.dependencies.depends import DependencyContainer

from src.core.auth.application.usecases import (
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase
)


auth_router = APIRouter(prefix="/api/v1", tags=["Auth"])


@auth_router.post("/auth/login", response_model=LoginResponseDTO)
@inject
async def login_user(
    user_data: LoginUserDTO,
    login_usecase: Annotated[
        LoginUserUseCase,
        Depends(
            Provide[
                DependencyContainer.login_usecase
            ]
        )
    ]
):
    return await login_usecase.execute(user_data)


@auth_router.post("/auth/refresh", response_model=LoginResponseDTO)
@inject
async def refresh_token(
    token_data: RefreshTokenDTO,
    refresh_usecase: Annotated[
        RefreshTokenUseCase,
        Depends(
            Provide[
                DependencyContainer.refresh_usecase
            ]
        )
    ]
):
    return await refresh_usecase.execute(token_data)


@auth_router.post("/auth/logout")
@inject
async def logout_user(
    token_data: RefreshTokenDTO,
    logout_usecase: Annotated[
        LogoutUserUseCase,
        Depends(
            Provide[
                DependencyContainer.logout_usecase
            ]
        )
    ]
):
    await logout_usecase.execute(token_data)
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