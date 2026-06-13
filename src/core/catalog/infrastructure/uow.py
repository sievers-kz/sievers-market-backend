from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.infrastructure.repositories import (
    CategoryRepository,
    RubricRepository,
    SubcategoryRepository,
)
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class CatalogUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def rubric(self) -> RubricRepository:
        return RubricRepository(self._session)

    @property
    def category(self) -> CategoryRepository:
        return CategoryRepository(self._session)

    @property
    def subcategory(self) -> SubcategoryRepository:
        return SubcategoryRepository(self._session)
