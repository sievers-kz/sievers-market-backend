from fastapi import APIRouter

from src.core.references.presentation.routers.brand import brand_router
from src.core.references.presentation.routers.color import color_router

router_list = [
    brand_router,
    color_router,
]

reference_router = APIRouter(prefix="/api/v1/reference", tags=["Reference"])
for router in router_list:
    reference_router.include_router(router)
