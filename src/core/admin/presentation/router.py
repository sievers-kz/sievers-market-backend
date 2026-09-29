from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends

from src.core.admin.domain.entities import Admin
from src.core.admin.presentation.dependencies import AdminServiceDependency
from src.core.admin.presentation.documentation import (
    CREATE_ADMIN_DOC,
    GRANT_PERMISSION_DOC,
)
from src.core.admin.presentation.dto import CreateAdminRequest, GrantPermissionRequest
from src.core.shared.presentation.security import require_admin

admin_router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@admin_router.post(
    "/",
    operation_id=CREATE_ADMIN_DOC.operation_id,
    summary=CREATE_ADMIN_DOC.summary,
    responses=CREATE_ADMIN_DOC.responses_doc,
    description=CREATE_ADMIN_DOC.description,
)
@inject
async def create_admin(
    dto: CreateAdminRequest,
    service: AdminServiceDependency,
    current_admin: Admin = Depends(require_admin("create:admin")),
):
    await service.create_admin(current_admin.account_id, dto)
    return {"message": "Администратор успешно создан"}


@admin_router.post(
    "/permission/grant",
    operation_id=GRANT_PERMISSION_DOC.operation_id,
    summary=GRANT_PERMISSION_DOC.summary,
    responses=GRANT_PERMISSION_DOC.responses_doc,
    description=GRANT_PERMISSION_DOC.description,
)
@inject
async def grant_permission(
    dto: GrantPermissionRequest,
    service: AdminServiceDependency,
    current_admin: Admin = Depends(require_admin("grant:permission")),
):
    await service.grant_permission(current_admin.account_id, dto)
    return {"message": "Права для администратора выданы"}
