from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import APIKeyCookie
from fastapi.security import HTTPAuthorizationCredentials as BearerCredentials
from fastapi.security import HTTPBearer

from src.configuration.dependencies.container import ApplicationContainer
from src.core.admin.domain.entities import Admin
from src.core.admin.domain.exceptions import (
    AdminProfileRequiredError,
    InsufficientPermissionsError,
)
from src.core.admin.infrastructure.uow import AdminUnitOfWork
from src.core.customer.application.usecases import GetOrCreateCustomerUseCase
from src.core.customer.domain.exceptions import OrganizationRequiredError
from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.iam.domain.enums import TokenType
from src.core.iam.domain.exceptions import (
    InvalidTokenError,
    InvalidTokenTypeError,
    TokenExpiredError,
)
from src.core.iam.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.iam.infrastructure.uow import IAMUnitOfWork
from src.core.shared.infrastructure.services.api_session_service import (
    APISessionService,
)
from src.core.shared.presentation.dto import (
    CurrentCustomer,
    CurrentOrganization,
    CurrentUser,
)

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="Введите JWT токен в формате: Bearer <токен>",
    auto_error=False,
)

cookie_scheme = APIKeyCookie(
    scheme_name="CookieAuth",
    name="access_token",
    auto_error=False,
)


@inject
def get_from_auth_scheme(
    token_from_bearer: Annotated[BearerCredentials | None, Depends(bearer_scheme)] = None,
    token_from_cookie: Annotated[str | None, Depends(cookie_scheme)] = None,
    client_type: Annotated[str | None, Header(alias="X-Client-Type")] = None,
    api_session_service: APISessionService = Depends(Provide[ApplicationContainer.shared.api_session_service]),
) -> str:
    return api_session_service.extract_token(token_from_bearer, token_from_cookie, client_type)


@inject
async def get_current_user_id(
    token: Annotated[str, Depends(get_from_auth_scheme)],
    token_service: PyJWTTokenService = Depends(Provide[ApplicationContainer.iam.pyjwt_token_service]),
) -> UUID:
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

    except (InvalidTokenTypeError, TokenExpiredError, InvalidTokenError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@inject
async def get_current_user(
    uow: IAMUnitOfWork = Depends(Provide[ApplicationContainer.iam.uow]),
    account_id: UUID = Depends(get_current_user_id),
):
    async with uow:
        account = await uow.account.get_account_by_id(account_id)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Аккаунт не найден",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return CurrentUser(id=account.id)


@inject
async def get_current_customer(
    usecase: Annotated[
        GetOrCreateCustomerUseCase, Depends(Provide[ApplicationContainer.customer.get_or_create_customer_usecase])
    ],
    account: CurrentUser = Depends(get_current_user),
):
    customer = await usecase.execute(account.id)
    return CurrentCustomer(id=customer.id)


@inject
async def get_current_organization(
    uow: Annotated[CustomerUnitOfWork, Depends(Provide[ApplicationContainer.customer.uow])],
    customer: CurrentCustomer = Depends(get_current_customer),
):
    async with uow:
        organization = await uow.organization.get_by_owner_id(customer.id)
        if not organization:
            raise OrganizationRequiredError()
        return CurrentOrganization(id=organization.id)


@inject
async def get_current_admin(
    uow: Annotated[AdminUnitOfWork, Depends(Provide[ApplicationContainer.admin.uow])],
    account: CurrentUser = Depends(get_current_user),
):
    async with uow:
        admin = await uow.admin.get_by_account_id(account.id)
        if not admin:
            raise AdminProfileRequiredError()
        return admin


def require_admin(permission_code: str):
    async def dependency(
        admin: Admin = Depends(get_current_admin),
    ) -> Admin:
        if not admin.can(permission_code):
            raise InsufficientPermissionsError()
        return admin

    return dependency
