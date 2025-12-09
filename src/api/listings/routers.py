from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security

from src.api.listings.dto import CreateListingDTO
from src.api.shared.security import get_current_user
from src.configuration.dependencies.depends import DependencyContainer
from src.core.listings.application.usecases import GetListingCreationSchemaUseCase, CreateListingUseCase
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
    listing_dto: CreateListingDTO,
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