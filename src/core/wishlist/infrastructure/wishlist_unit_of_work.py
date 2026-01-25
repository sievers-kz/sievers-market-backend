from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork
from src.core.wishlist.infrastructure.repository import WishlistRepository


class WishlistUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def wishlist(self) -> WishlistRepository:
        return WishlistRepository(self._session)
