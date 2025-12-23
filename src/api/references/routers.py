from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.references.dto import RoubricResponse
from src.core.references.application.usecases.categories_tree import GetCategoriesTreeUseCase


reference = APIRouter(prefix="/api/v1/references", tags=["References"])


@reference.get("/categories/tree", response_model=RoubricResponse)
@inject
async def get_category_tree(
    get_category_tree_usecase: Annotated[
        GetCategoriesTreeUseCase,
        Depends(
            Provide["reference.get_category_tree_usecase"]
        )
    ]
):
    return await get_category_tree_usecase.execute()
