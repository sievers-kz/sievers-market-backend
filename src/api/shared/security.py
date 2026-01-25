from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status, Depends
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.api.shared.dto import CurrentUser, CurrentSeller, CurrentBuyer
from src.configuration.dependencies.container import ApplicationContainer
from src.core.buyer.application.interfaces.abstract_buyer_uow import AbstractBuyerUnitOfWork
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.domain.enums import TokenType, UserRole
from src.core.iam.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.seller.application.interfaces.abstract_seller_uow import AbstractSellerUnitOfWork

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
        Provide[
            ApplicationContainer.iam.pyjwt_token_service
        ]
    ),
) -> UUID:
    token = credentials.credentials

    try:
        payload = token_service.verify_token(token, TokenType.ACCESS)
        account_id_from_jwt = payload.get("sub")

        if not account_id_from_jwt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Невалидный или просроченный токен",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return UUID(account_id_from_jwt)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Невалидный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"}
        ) from exc


@inject
async def get_current_user(
    unit_of_work: AbstractIAMUnitOfWork
    = Depends(
        Provide[
            ApplicationContainer.iam.iam_unit_of_work
        ]
    ),
    account_id: UUID = Depends(get_current_user_id)
):
    async with unit_of_work as uow:
        account = await uow.account.get_account_by_id(account_id)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return CurrentUser(id=account.id, role=account.role)


@inject
async def get_current_buyer(
    unit_of_work: Annotated[
        AbstractBuyerUnitOfWork,
        Depends(
            Provide[
                ApplicationContainer.buyer.buyer_unit_of_work
            ]
        )
    ],
    account: CurrentUser = Depends(get_current_user)
):
    if account.role != UserRole.BUYER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
            headers={"WWW-Authenticate": "Bearer"}
        )

    async with unit_of_work as uow:
        buyer = await uow.buyer.get_by_account_id(account.id)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buyer not found"
            )

        return CurrentBuyer(id=buyer.id)


@inject
async def get_current_seller(
    unit_of_work: Annotated[
        AbstractSellerUnitOfWork,
        Depends(
            Provide[
                ApplicationContainer.seller.seller_unit_of_work
            ]
        )
    ],
    account: CurrentUser = Depends(get_current_user)
):
    if account.role != UserRole.SELLER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
            headers={"WWW-Authenticate": "Bearer"}
        )

    async with unit_of_work as uow:
        seller = await uow.seller.get_by_account_id(account.id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found"
            )

        return CurrentSeller(id=seller.id)

