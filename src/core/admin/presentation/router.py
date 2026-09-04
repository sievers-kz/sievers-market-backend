from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends, Security

from src.configuration.dependencies.container import ApplicationContainer
from src.core.admin.application.services.admin_service import AdminService
from src.core.admin.presentation.dto import CreateAdminRequest
from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user

admin_router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@admin_router.post("/")
@inject
async def create_admin(
    dto: CreateAdminRequest,
    service: Annotated[
        AdminService, Depends(Provide[ApplicationContainer.admin.admin_service])
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    await service.create_admin(current_user.id, dto)
