from typing import Annotated
from uuid import UUID

from fastapi import Header, HTTPException, status, Depends
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.exceptions.exception_classes import InvalidTokenError
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService

from src.core.users.application.abstract_user_uow import AbstractUserUnitOfWork


bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="Введите JWT токен в формате: Bearer <токен>",
    auto_error=True
)


@inject
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_service: AbstractTokenService
    = Depends(
        Provide["iam.token_service"]
    ),
) -> UUID:
    token = credentials.credentials

    try:
        payload = token_service.verify_token(token, TokenTypeEnum.ACCESS_TOKEN)
        user_id_from_jwt = payload.get("sub")

        if not user_id_from_jwt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Невалидный или просроченный токен",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return UUID(user_id_from_jwt)

    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Невалидный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"}
        ) from exc


@inject
async def get_current_user(
    unit_of_work: AbstractUserUnitOfWork
    = Depends(
        Provide["iam.user_unit_of_work"]
    ),
    user_id: UUID = Depends(get_current_user_id)
):
    async with unit_of_work as uow:
        user = await uow.user.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return user
