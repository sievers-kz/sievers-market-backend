from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.users.user_dto import (
    UserDTO,
    EmailConfirmationDTO,
    ResetPasswordDTO
)

from src.configuration.dependencies.depends import DependencyContainer

from src.core.users.application.usecases import (
    EmailConfirmationUseCase,
    ResetPasswordUseCase,
    RegisterUserUseCase,
)


users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.post("/auth/register")
@inject
async def register_user(
    user_data: UserDTO,
    register_usecase: Annotated[
        RegisterUserUseCase,
        Depends(
            Provide[
                DependencyContainer.register_usecase
            ]
        )
    ]
):
    await register_usecase.execute(user_dto=user_data)
    return {"message": "Регистрация прошла успешно. Пожалуйста, подтвердите свою почту для завершения"}


@users_router.post("/auth/email_confirmation")
@inject
async def confirm_email(
    confirmation_code: EmailConfirmationDTO,
    confirmation_usecase: Annotated[
        EmailConfirmationUseCase,
        Depends(
            Provide[
                DependencyContainer.confirmation_usecase
            ]
        )
    ]
):
    await confirmation_usecase.execute(confirmation_code)
    return {"message": "Ваша электронная почта успешно подтверждена!"}


@users_router.post("/auth/reset-password")
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

