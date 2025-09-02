import uvicorn
from fastapi import FastAPI

from src.api.users.user_routers import users_router
from src.configuration.conf.settings import DatabaseConnectionSettings
from src.configuration.dependencies.depends import DependencyContainer


def create_fastapi_app() -> FastAPI:
    container = DependencyContainer()
    settings = DatabaseConnectionSettings()
    container.config.from_pydantic(settings)

    app = FastAPI(title="AGROW Marketplace")
    app.container = container
    app.include_router(users_router)
    return app


fastapi_app = create_fastapi_app()



