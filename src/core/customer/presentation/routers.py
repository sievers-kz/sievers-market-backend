from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security
from typing_extensions import Annotated

from src.core.customer.presentation.dto import ChangeCustomerFullname, CustomerResponse
from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user
from src.configuration.dependencies.container import ApplicationContainer

from src.core.customer.application.usecases import (
    ChangeCustomerFullnameUseCase,
    GetCurrentCustomerUseCase,
)


customer = APIRouter(prefix="/api/v1/customer", tags=["Customer"])


@customer.get("/me", response_model=CustomerResponse)
@inject
async def get_current_customer(
    usecase: Annotated[
        GetCurrentCustomerUseCase,
        Depends(
            Provide[
                ApplicationContainer.customer.get_current_customer_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    return await usecase.execute(current_user.id)


@customer.patch("/me/change-fullname")
@inject
async def change_customer_fullname(
    dto: ChangeCustomerFullname,
    usecase: Annotated[
        ChangeCustomerFullnameUseCase,
        Depends(
            Provide[
                ApplicationContainer.customer.change_customer_fullname_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Ваши данные успешно изменены!"}


