from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.api.shared.exceptions.exception_handlers import application_exception_handler, pydantic_exception_handler
from src.api.auth.auth_routers import auth_router
from src.api.users.user_routers import users_router
from src.core.shared.application.exceptions.base_exception import BaseApplicationError
from src.configuration.conf.settings import DatabaseConnectionSettings
from src.configuration.dependencies.depends import DependencyContainer


def create_fastapi_app() -> FastAPI:
    container = DependencyContainer()
    settings = DatabaseConnectionSettings()
    container.config.from_pydantic(settings)

    app = FastAPI(title="AGROW Marketplace")
    app.container = container

    app.add_exception_handler(BaseApplicationError, application_exception_handler)
    app.add_exception_handler(RequestValidationError, pydantic_exception_handler)

    app.include_router(users_router)
    app.include_router(auth_router)

    return app


fastapi_app = create_fastapi_app()



