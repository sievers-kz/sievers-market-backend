from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security

from src.api.listings.dto import CreateActiveListingDTO, UpdateListingDTO, CreateDraftListingDTO
from src.api.shared.security import get_current_user
from src.configuration.dependencies.depends import DependencyContainer
from src.core.listings.application.usecases import GetListingCreationSchemaUseCase, CreateListingUseCase, \
    UpdateListingSchemaUseCase, UpdateListingUseCase, GetUserListingsUseCase, CreateDraftListingUseCase
from src.core.listings.domain.enums import ListingStatusEnum
from src.core.users.domain.entities import User

listings = APIRouter(prefix="/api/v1/listings", tags=["Listings"])


@listings.get("/create/schema/{subcategory_id}")
@inject
async def get_listing_creation_schema(
    subcategory_id: UUID,
    listing_creation_schema_usecase: Annotated[
        GetListingCreationSchemaUseCase,
        Depends(
            Provide[
                DependencyContainer.listing_creation_schema_usecase
            ]
        )
    ],
    current_user: User = Security(get_current_user)
):
    return await listing_creation_schema_usecase.execute(subcategory_id)


@listings.post("/create/new")
@inject
async def create_new_listing(
    listing_dto: CreateActiveListingDTO,
    create_listing_usecase: Annotated[
        CreateListingUseCase,
        Depends(
            Provide[
                DependencyContainer.create_listing_usecase
            ]
        )
    ],
    current_user: User = Security(get_current_user)
):
    await create_listing_usecase.execute(listing_dto, current_user.id)
    return {"message": "Ваше объявление создано"}


@listings.get("/update/schema/{listing_id}")
@inject
async def get_listing_update_schema(
    listing_id: UUID,
    update_listing_schema_usecase: Annotated[
        UpdateListingSchemaUseCase,
        Depends(
            Provide[
                DependencyContainer.update_listing_schema_usecase
            ]
        )
    ],
    current_user: User = Security(get_current_user)
):
    return await update_listing_schema_usecase.execute(listing_id)


@listings.patch("/update/listing/{listing_id}")
@inject
async def update_current_listing(
    update_listing_dto: UpdateListingDTO,
    listing_id: UUID,
    update_listing_usecase: Annotated[
        UpdateListingUseCase,
        Depends(
            Provide[
                DependencyContainer.update_listing_usecase
            ]
        )
    ],
    current_user: User = Security(get_current_user)
):
    await update_listing_usecase.execute(update_listing_dto, listing_id)
    return {"message": "Объявление успешно изменено"}


@listings.get("/me/listings/{status}")
@inject
async def get_user_listings(
    status: ListingStatusEnum,
    get_user_listings_usecase: Annotated[
        GetUserListingsUseCase,
        Depends(
            Provide[
                DependencyContainer.get_user_listings_usecase
            ]
        )
    ],
    current_user: User = Security(get_current_user)
):
    return await get_user_listings_usecase.execute(status, current_user.id)


@listings.post("/create/draft")
@inject
async def create_draft_listing(
    draft_dto: CreateDraftListingDTO,
    create_draft_listing_usecase: Annotated[
        CreateDraftListingUseCase,
        Depends(
            Provide[
                DependencyContainer.create_draft_listing_usecase
            ]
        )
    ],
    current_user: User = Security(get_current_user)
):
    await create_draft_listing_usecase.execute(draft_dto, current_user.id)
    return {"message": "Объявление сохранено в черновик"}
