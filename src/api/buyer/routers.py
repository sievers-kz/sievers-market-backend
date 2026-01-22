from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security
from typing_extensions import Annotated

from src.api.buyer.dto import ChangeFullname, ChangeBuyerRegion, BuyerResponse
from src.api.shared.dto import CurrentUser
from src.api.shared.security import get_current_user
from src.configuration.dependencies.container import ApplicationContainer

from src.core.buyer.application.usecases import (
    ChangeFullnameUseCase,
    ChangeBuyerRegionUseCase,
    GetCurrentBuyerUseCase
)


buyer = APIRouter(prefix="/api/v1/buyer", tags=["Buyer"])


@buyer.get("/me", response_model=BuyerResponse, operation_id="getCurrentBuyer")
@inject
async def get_current_buyer(
    usecase: Annotated[
        GetCurrentBuyerUseCase,
        Depends(
            Provide[
                ApplicationContainer.buyer.get_current_buyer_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    return await usecase.execute(current_user.id)


@buyer.patch("/me/change-fullname")
@inject
async def change_fullname(
    dto: ChangeFullname,
    usecase: Annotated[
        ChangeFullnameUseCase,
        Depends(
            Provide[
                ApplicationContainer.buyer.change_fullname_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваши данные успешно изменены!"}


@buyer.patch("/me/change-region", operation_id="changeBuyerRegion")
@inject
async def change_buyer_region(
    dto: ChangeBuyerRegion,
    usecase: Annotated[
        ChangeBuyerRegionUseCase,
        Depends(
            Provide[
                ApplicationContainer.buyer.change_buyer_region_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваш регион изменен"}
