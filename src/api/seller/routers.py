from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security
from typing_extensions import Annotated

from src.api.seller.dto import SellerFullnameData, TaxIDData, BecomeSellerData, \
    SellerResponse, CompanyNameData
from src.api.shared.dto import CurrentUser
from src.api.shared.security import get_current_user
from src.configuration.dependencies.container import ApplicationContainer

from src.core.seller.application.usecases import (
    ChangeFullnameUseCase,
    ChangeCompanyNameUseCase,
    ChangeTaxIDUseCase,
    BecomeSellerUseCase,
    GetCurrentSellerUseCase
)


seller = APIRouter(prefix="/api/v1/seller", tags=["Seller"])


@seller.get("/me", response_model=SellerResponse, operation_id="getCurrentSeller")
@inject
async def get_current_seller(
    usecase: Annotated[
        GetCurrentSellerUseCase,
        Depends(
            Provide[
                ApplicationContainer.seller.get_current_seller_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    return await usecase.execute(current_user.id)


@seller.patch("/me/change-fullname", operation_id="changeSellerFullname")
@inject
async def change_fullname(
    dto: SellerFullnameData,
    usecase: Annotated[
        ChangeFullnameUseCase,
        Depends(
            Provide[
                ApplicationContainer.seller.change_fullname_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Fullname changed successfully"}


@seller.patch("/me/change-company-name")
@inject
async def change_company_name(
    dto: CompanyNameData,
    usecase: Annotated[
        ChangeCompanyNameUseCase,
        Depends(
            Provide[
                ApplicationContainer.seller.change_company_name_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Company name changed successfully"}


@seller.patch("/me/change-tax-id")
@inject
async def change_tax_id(
    dto: TaxIDData,
    usecase: Annotated[
        ChangeTaxIDUseCase,
        Depends(
            Provide[
                "seller.change_tax_id_usecase"
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Tax ID changed successfully"}


@seller.post("/me/become-seller")
@inject
async def become_seller(
    dto: BecomeSellerData,
    usecase: Annotated[
        BecomeSellerUseCase,
        Depends(
            Provide[
                "seller.become_seller_usecase"
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "You are now a seller!"}