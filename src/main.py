from fastapi import FastAPI

from src.api.customer.routers import customer
from src.api.iam.routers import iam
from src.core.machinery.presentation.routers import machinery
from src.api.reference.routers import reference
from src.api.wishlist.routers import wishlist
from src.api.media.routers import media
from src.configuration.dependencies.container import ApplicationContainer


def create_fastapi_app() -> FastAPI:
    app = FastAPI(title="AGROW Marketplace", version="1.0.0")
    container = ApplicationContainer()
    container.wire(
        modules=[
            "src.api.iam.routers",
            "src.api.customer.routers",
            "src.core.machinery.presentation.routers",
            "src.api.reference.routers",
            "src.api.shared.security",
            "src.api.wishlist.routers",
            "src.api.media.routers"
        ]
    )
    app.container = container

    app.include_router(iam)
    app.include_router(customer)
    app.include_router(reference)
    app.include_router(machinery)
    app.include_router(wishlist)
    app.include_router(media)

    return app


fastapi_app = create_fastapi_app()
