from fastapi import FastAPI

from src.api.buyer.routers import buyer
from src.api.iam.routers import iam
from src.api.machinery.routers import machinery
from src.api.reference.routers import reference
from src.api.seller.routers import seller
from src.api.wishlist.routers import wishlist
from src.configuration.dependencies.container import ApplicationContainer


def create_fastapi_app() -> FastAPI:
    app = FastAPI(title="AGROW Marketplace", version="1.0.0")
    container = ApplicationContainer()
    container.wire(
        modules=[
            "src.api.iam.routers",
            "src.api.buyer.routers",
            "src.api.seller.routers",
            "src.api.machinery.routers",
            "src.api.reference.routers",
            "src.api.shared.security",
            "src.api.wishlist.routers"
        ]
    )
    app.container = container

    app.include_router(iam)
    app.include_router(buyer)
    app.include_router(seller)
    app.include_router(reference)
    app.include_router(machinery)
    app.include_router(wishlist)

    return app


fastapi_app = create_fastapi_app()
