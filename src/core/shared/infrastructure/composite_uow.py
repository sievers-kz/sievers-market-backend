from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.infrastructure.auth_repository import UserIdentityRepository
from src.core.listings.infrastructure.repository import ListingRepository, ListingQueryService
from src.core.references.infrastructure.repository import ReferenceRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork
from src.core.users.infrastructure.user_repository import UserRepository


class UserIdentityUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def user(self):
        return UserRepository(self._session)

    @property
    def identity(self):
        return UserIdentityRepository(self._session)


class CompositeListingReferenceUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory)

    @property
    def listing(self):
        return ListingRepository(self._session)

    @property
    def listing_query(self):
        return ListingQueryService(self._session)

    @property
    def reference(self):
        return ReferenceRepository(self._session)



