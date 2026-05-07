from src.core.catalog.application.interfaces import ICatalogUnitOfWork


class CategoryService:
    def __init__(self, uow: ICatalogUnitOfWork):
        self.uow = uow

