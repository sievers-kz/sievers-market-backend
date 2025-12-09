from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.references.infrastructure.repository import ReferenceRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class ReferenceUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def reference(self):
        if self._session is None:
            raise RuntimeError("UoW not initialized!")
        return ReferenceRepository(self._session)


