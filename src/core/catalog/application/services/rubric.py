from src.core.catalog.application.interfaces.uow import ICatalogUnitOfWork


class RubricService:
    def __init__(self, uow: ICatalogUnitOfWork):
        self.uow = uow


