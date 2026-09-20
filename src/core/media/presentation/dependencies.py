from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.media.application.services.media_service import MediaService

MediaServiceDependency = Annotated[MediaService, Depends(Provide[ApplicationContainer.media.media_service])]
