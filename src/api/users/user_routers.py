from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.users.user_dto import (
    CreateUserDTO,
    EmailConfirmationDTO,
    ResetPasswordDTO
)

from src.configuration.dependencies.depends import DependencyContainer

from src.core.users.application.usecases import (
    CreateUserUseCase,
    EmailConfirmationUseCase,
    ResetPasswordUseCase
)


users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.post("/auth/registration/")
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


@users_router.post("/auth/email_confirmation")
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
