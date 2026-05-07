from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference, Theme, Layout

from src.core.catalog.presentation.routers.catalog import catalog_router
from src.core.customer.presentation.routers import customer
from src.core.iam.presentation.routers import iam
from src.core.machinery.presentation.routers import machinery
from src.core.references.presentation.routers.reference import reference_router
from src.core.wishlist.presentation.routers import wishlist
from src.core.media.presentation.routers import media
from src.configuration.dependencies.container import ApplicationContainer


class ApplicationFactory:
    def __init__(self):
        self.app = FastAPI(
            title="AGROW Marketplace",
            version="1.0.0",
        )
        self.container = ApplicationContainer()

    def _wire_dependency(self):
        self.container.wire(
            modules=[
                "src.core.iam.presentation.routers",
                "src.core.customer.presentation.routers",
                "src.core.machinery.presentation.routers",
                "src.core.shared.presentation.security",
                "src.core.wishlist.presentation.routers",
                "src.core.media.presentation.routers",
            ],
            packages=[
                "src.core.catalog.presentation.routers",
                "src.core.references.presentation.routers",
            ]
        )
        self.app.container = self.container

    def _include_routers(self):
        routers = [
            iam,
            customer,
            reference_router,
            wishlist,
            media,
            catalog_router,
            machinery,
        ]
        for router in routers:
            self.app.include_router(router)

    def _setup_docs(self):
        @self.app.get("/scalar", include_in_schema=False)
        async def scalar_html():
            return get_scalar_api_reference(
                openapi_url=self.app.openapi_url,
                title=self.app.title,
                theme=Theme.MARS,
                layout=Layout.MODERN
            )

    def build(self) -> FastAPI:
        self._wire_dependency()
        self._include_routers()
        self._setup_docs()
        return self.app


fastapi_app = ApplicationFactory().build()
