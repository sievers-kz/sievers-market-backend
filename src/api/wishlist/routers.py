from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security

from src.api.shared.dto import CurrentBuyer
from src.api.shared.security import get_current_buyer
from src.api.wishlist.dto import WishlistCard
from src.configuration.dependencies.container import ApplicationContainer
from src.core.wishlist.application.usecases import AddToWishlistUseCase, DeleteFromWishlistUseCase, GetWishlistUseCase

wishlist = APIRouter(prefix="/api/v1/wishlist", tags=["Wishlist"])


@wishlist.post("/add/{machinery_id}")
@inject
async def add_to_wishlist(
    machinery_id: UUID,
    usecase: Annotated[
        AddToWishlistUseCase,
        Depends(
            Provide[
                ApplicationContainer.wishlist.add_to_wishlist_usecase
            ]
        )
    ],
    current_buyer: CurrentBuyer = Security(get_current_buyer)
):
    await usecase.execute(current_buyer.id, machinery_id)
    return {"message": "Added to wishlist successfully"}


@wishlist.delete("/remove/{machinery_id}")
@inject
async def delete_from_wishlist(
    machinery_id: UUID,
    usecase: Annotated[
        DeleteFromWishlistUseCase,
        Depends(
            Provide[
                ApplicationContainer.wishlist.delete_from_wishlist_usecase
            ]
        )
    ],
    current_buyer: CurrentBuyer = Security(get_current_buyer)
):
    await usecase.execute(current_buyer.id, machinery_id)
    return {"message": "Removed from wishlist successfully"}


@wishlist.get("/list", response_model=list[WishlistCard])
@inject
async def get_wishlist(
    usecase: Annotated[
        GetWishlistUseCase,
        Depends(
            Provide[
                ApplicationContainer.wishlist.get_wishlist_usecase
            ]
        )
    ],
    current_buyer: CurrentBuyer = Security(get_current_buyer)
):
    return await usecase.execute(current_buyer.id)
