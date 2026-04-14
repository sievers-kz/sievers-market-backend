from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.params import Query
from fastapi_filter import FilterDepends

from src.core.shared.presentation.dto import CurrentCustomer
from src.core.shared.presentation.security import get_current_customer
from src.configuration.dependencies.container import ApplicationContainer

from src.core.machinery.application.usecases import (
    CreateMachineryUseCase,
    GetMachineryListUseCase,
    GetMachineryDetailUseCase,
    GetCustomerMachineryUseCase,
    ActivateMachineryUseCase,
    DeactivateMachineryUseCase,
    ArchiveMachineryUseCase,
    DeleteMachineryUseCase,
    GetCustomerMachineryDetailUseCase,
    ChangeMachineryGeneralUseCase,
    ChangeOperatingHistoryUseCase,
    ChangeMachineryPriceUseCase,
    ChangeMachinerySpecUseCase,
    ChangeMachineryDescriptionUseCase
)

from src.core.machinery.presentation.dto import (
    CreateMachineryRequest,
    PaginatedMachinery,
    MachineryDetailQuery,
    MachineryOwnerDetailQuery,
    ChangeMachineryPriceRequest,
    ChangeMachineryGeneralRequest,
    ChangeOperatingHistoryRequest,
    ChangeMachinerySpecRequest,
    ChangeMachineryDescriptionRequest
)

from src.core.machinery.presentation.filters import MachineryFilter, MachineryOwnerFilter


machinery = APIRouter(prefix="/api/v1/machinery", tags=["Machinery"])


@machinery.post("/create")
@inject
async def create_machinery(
    dto: CreateMachineryRequest,
    usecase: Annotated[
        CreateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.create_machinery_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(current_customer.id, dto)
    return {"message": "Listing successfully created"}


@machinery.get("/", response_model=PaginatedMachinery)
@inject
async def get_machinery_list(
    usecase: Annotated[
        GetMachineryListUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_machinery_list_usecase
            ]
        )
    ],

    machinery_filter: MachineryFilter = FilterDepends(MachineryFilter),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1)
):
    return await usecase.execute(
        filters=machinery_filter,
        page=page,
        limit=limit
    )


@machinery.get("/detail/{machinery_id}", response_model=MachineryDetailQuery)
@inject
async def get_machinery_detail(
    machinery_id: UUID,
    usecase: Annotated[
        GetMachineryDetailUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_machinery_detail_usecase
            ]
        )
    ]
):
    return await usecase.execute(machinery_id)


@machinery.get("/me/", response_model=PaginatedMachinery)
@inject
async def get_customer_machinery(
    usecase: Annotated[
        GetCustomerMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_customer_machinery_usecase
            ]
        )
    ],
    machinery_owner_filter: MachineryOwnerFilter = FilterDepends(MachineryOwnerFilter),
    current_customer: CurrentCustomer = Depends(get_current_customer),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1)
):
    return await usecase.execute(current_customer.id, machinery_owner_filter, page, limit)


@machinery.patch("/activate/{machinery_id}")
@inject
async def activate_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        ActivateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.activate_machinery_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(current_customer.id, machinery_id)
    return {"message": "Listing successfully activated"}


@machinery.patch("/deactivate/{machinery_id}")
@inject
async def deactivate_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        DeactivateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.deactivate_machinery_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(current_customer.id, machinery_id)
    return {"message": "Listing successfully deactivated"}


@machinery.patch("/archive/{machinery_id}")
@inject
async def archive_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        ArchiveMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.archive_machinery_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(current_customer.id, machinery_id)
    return {"message": "Listing successfully archived"}


@machinery.patch("/delete/{machinery_id}")
@inject
async def delete_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        DeleteMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.delete_machinery_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(current_customer.id, machinery_id)
    return {"message": "Listing successfully deleted"}


@machinery.get("/me/detail/{machinery_id}", response_model=MachineryOwnerDetailQuery)
@inject
async def get_customer_machinery_detail(
    machinery_id: UUID,
    usecase: Annotated[
        GetCustomerMachineryDetailUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_customer_machinery_detail_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    return await usecase.execute(current_customer.id, machinery_id)


@machinery.patch("/change/general/{machinery_id}")
@inject
async def change_general_machinery(
    machinery_id: UUID,
    dto: ChangeMachineryGeneralRequest,
    usecase: Annotated[
        ChangeMachineryGeneralUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.change_machinery_general_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(machinery_id, dto)
    return {"message": "Listing successfully changed"}


@machinery.patch("/change/operating-history/{machinery_id}")
@inject
async def change_operating_history(
    machinery_id: UUID,
    dto: ChangeOperatingHistoryRequest,
    usecase: Annotated[
        ChangeOperatingHistoryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.change_operating_history_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(machinery_id, dto)
    return {"message": "Listing successfully changed"}


@machinery.patch("/change/price/{machinery_id}")
@inject
async def change_machinery_price(
    machinery_id: UUID,
    dto: ChangeMachineryPriceRequest,
    usecase: Annotated[
        ChangeMachineryPriceUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.change_machinery_price_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(machinery_id, dto)
    return {"message": "Listing successfully updated"}


@machinery.patch("/change/specification/{machinery_id}")
@inject
async def change_machinery_specification(
    machinery_id: UUID,
    dto: ChangeMachinerySpecRequest,
    usecase: Annotated[
        ChangeMachinerySpecUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.change_machinery_spec_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(machinery_id, dto)
    return {"message": "Listing successfully updated"}


@machinery.patch("/change/description/{machinery_id}")
@inject
async def change_machinery_description(
    machiney_id: UUID,
    dto: ChangeMachineryDescriptionRequest,
    usecase: Annotated[
        ChangeMachineryDescriptionUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.change_machinery_description_usecase
            ]
        )
    ],
    current_customer: CurrentCustomer = Depends(get_current_customer)
):
    await usecase.execute(machiney_id, dto)
    return {"message": "Listing successfully updated"}
