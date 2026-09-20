from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.admin.application.services.admin_service import AdminService

AdminServiceDependency = Annotated[AdminService, Depends(Provide[ApplicationContainer.admin.admin_service])]
