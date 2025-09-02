from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.users.user_dto import UserDTO
from src.configuration.dependencies.depends import DependencyContainer
from src.core.users.application.usecases import RegisterUserUseCase

users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.post("/auth/register")
@inject
async def register_user(
    user_data: UserDTO,
    register_usecase: Annotated[
        RegisterUserUseCase,
        Depends(Provide[DependencyContainer.register_usecase])
    ]
):
    await register_usecase.execute(user_dto=user_data)
    return {"message": "success"}