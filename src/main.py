from fastapi import FastAPI

from src.core.customer.presentation.routers import customer
from src.core.iam.presentation.routers import iam
from src.core.machinery.presentation.routers import machinery
from src.core.references.presentation.routers import reference
from src.core.wishlist.presentation.routers import wishlist
from src.core.media.presentation.routers import media
from src.configuration.dependencies.container import ApplicationContainer


def create_fastapi_app() -> FastAPI:
    app = FastAPI(title="AGROW Marketplace", version="1.0.0")
    container = ApplicationContainer()
    container.wire(
        modules=[
            "src.core.iam.presentation.routers",
            "src.core.customer.presentation.routers",
            "src.core.machinery.presentation.routers",
            "src.core.references.presentation.routers",
            "src.core.shared.presentation.security",
            "src.core.wishlist.presentation.routers",
            "src.core.media.presentation.routers",
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

