from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.infrastructure.repositories import (
    BrandRepository,
    ColorRepository,
)
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class ReferenceUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def brand(self):
        return BrandRepository(self._session)

    @property
    def color(self):
        return ColorRepository(self._session)
