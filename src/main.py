from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.api.auth.auth_routers import auth_router
from src.api.listings.routers import listings
from src.api.references.routers import reference
from src.api.shared.exceptions.exception_handlers import application_exception_handler, pydantic_exception_handler
from src.api.shared.security import bearer_scheme
from src.api.users.user_routers import users_router
from src.core.shared.application.exceptions.base_exception import BaseApplicationError
from src.configuration.conf.settings import DatabaseConnectionSettings
from src.configuration.dependencies.depends import DependencyContainer
from src.core.listings.infrastructure.models.events import update_listing_search_index


def create_fastapi_app() -> FastAPI:
    settings = DatabaseConnectionSettings()

    container = DependencyContainer()
    container.config.from_pydantic(settings)

    app = FastAPI(
        title="AGROW Marketplace",
        version="1.0.0",
    )
    app.container = container

    app.add_exception_handler(BaseApplicationError, application_exception_handler)
    app.add_exception_handler(RequestValidationError, pydantic_exception_handler)

    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(reference)
    app.include_router(listings)

    return app


fastapi_app = create_fastapi_app()


