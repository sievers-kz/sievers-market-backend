from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.references.dto import RoubricResponse
from src.configuration.dependencies.depends import DependencyContainer
from src.core.references.application.usecases.categories_tree import GetCategoriesTreeUseCase


reference = APIRouter(prefix="/api/v1/references", tags=["References"])


@reference.get("/categories/tree", response_model=RoubricResponse)
@inject
async def get_categories_tree(
    get_categories_tree_usecase: Annotated[
        GetCategoriesTreeUseCase,
        Depends(
            Provide[
                DependencyContainer.get_categories_tree_usecase
            ]
        )
    ]
):
    return await get_categories_tree_usecase.execute()
