from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.configuration.dependencies.container import ApplicationContainer
from src.core.customer.application.interfaces.uow import ICustomerUnitOfWork
from src.core.iam.application.interfaces.uow import IIAMUnitOfWork
from src.core.iam.domain.enums import TokenType
from src.core.iam.infrastructure.services.pyjwt_token import ITokenService
from src.core.shared.presentation.dto import CurrentCustomer, CurrentUser, CurrentVendor
from src.core.vendor.application.interfaces.uow import IVendorUnitOfWork

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="Введите JWT токен в формате: Bearer <токен>",
    auto_error=True,
)


@inject
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_service: ITokenService = Depends(
        Provide[ApplicationContainer.iam.pyjwt_token_service]
    ),
) -> UUID:
    token = credentials.credentials

    try:
        payload = token_service.verify_token(token, TokenType.ACCESS)
        account_id_from_jwt = payload.get("sub")

        if not account_id_from_jwt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный или просроченный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return UUID(account_id_from_jwt)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@inject
async def get_current_user(
    unit_of_work: IIAMUnitOfWork = Depends(
        Provide[ApplicationContainer.iam.iam_unit_of_work]
    ),
    account_id: UUID = Depends(get_current_user_id),
):
    async with unit_of_work as uow:
        account = await uow.account.get_account_by_id(account_id)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return CurrentUser(id=account.id)


@inject
async def get_current_customer(
    unit_of_work: Annotated[
        ICustomerUnitOfWork, Depends(Provide[ApplicationContainer.customer.uow])
    ],
    account: CurrentUser = Depends(get_current_user),
):
    async with unit_of_work as uow:
        customer = await uow.customer.get_by_account_id(account.id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )

        return CurrentCustomer(id=customer.id)


@inject
async def get_current_vendor(
    uow: Annotated[
        IVendorUnitOfWork, Depends(Provide[ApplicationContainer.vendor.uow])
    ],
    account: CurrentUser = Depends(get_current_user),
):
    async with uow:
        vendor = await uow.vendor.get_by_account_id(account.id)
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not registered as a vendor"
                " or your status is pending moderation",
            )

        return CurrentVendor(id=vendor.id)
