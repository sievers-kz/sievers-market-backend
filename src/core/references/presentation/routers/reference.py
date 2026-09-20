from fastapi import APIRouter

from src.core.references.presentation.routers.brand import brand_router
from src.core.references.presentation.routers.city import city_router
from src.core.references.presentation.routers.color import color_router
from src.core.references.presentation.routers.country import origin_country_router

router_list = [brand_router, color_router, origin_country_router, city_router]

reference_router = APIRouter(prefix="/api/v1/reference")
for router in router_list:
    reference_router.include_router(router)
