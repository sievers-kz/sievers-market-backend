import uuid

from sqlalchemy import select, inspect
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.users.domain.entities import UserAggregate, AuthTokenAggregate
from src.core.users.domain.enums import TokenTypeEnum
from src.core.users.domain.interfaces import AbstractRepository
from src.core.users.infrastructure.exceptions.exception_classes import UniqueConstraintError, RepositoryError
from src.core.users.infrastructure.mappers import UserMapper, AuthTokenMapper
from src.configuration.database.models.users import User, AuthToken


class UserRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> "":
        statement = (
            select(User)
            .options(
                joinedload(User.individual_profile),
                joinedload(User.business_profile),
                joinedload(User.auth)
            ).where(User.id == user_id)
        )

        result = await self.session.execute(statement)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return UserMapper.to_domain(user_model)

    async def save(self, user: UserAggregate) -> None:
        try:
            user_orm = UserMapper.to_orm(user)
            await self.session.merge(user_orm)
            await self.session.flush()

        except IntegrityError as exc:
            error_message = str(exc).lower()

            if "users_email_key" in error_message:
                raise UniqueConstraintError(
                    code="unique_violation",
                    details=error_message,
                    context={
                        "field": "email",
                        "verbose_name": "email",
                        "table": "users"
                    }
                ) from exc

            if "users_phone_key" in error_message:
                raise UniqueConstraintError(
                    code="unique_violation",
                    details=error_message,
                    context={
                        "field": "phone",
                        "verbose_name": "номер телефона",
                        "table": "users"
                    }
                ) from exc

        except SQLAlchemyError as exc:
            raise RepositoryError(
                code="unexpected_error",
                details=str(exc),
                context={
                    "operation": "save",
                    "table": "users"
                }
            ) from exc

    async def get_by_email(self, email: str) -> UserAggregate:
        statement = (
            select(User)
            .options(
                joinedload(User.individual_profile),
                joinedload(User.business_profile),
                joinedload(User.auth)
            ).where(User.email == email)
        )

        result = await self.session.execute(statement)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return UserMapper.to_domain(user_model)


class AuthTokenRepository: # FIXME: Set a simple validation if result return None
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_value(self, token_value: str) -> AuthTokenAggregate:
        statement = select(AuthToken).where(AuthToken.token_value == token_value)
        query_result = await self._session.execute(statement)
        token_model = query_result.scalar_one_or_none()

        if token_model is None:
            return None

        return AuthTokenMapper.to_domain(token_model)

    async def find_by_user_id(self, user_id: uuid.UUID) -> list[AuthTokenAggregate]:
        statement = select(AuthToken).where(AuthToken.user_id == user_id)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalars().all())

    async def find_by_token_id(self, token_id: uuid.UUID) -> AuthTokenAggregate:
        statement = select(AuthToken).where(AuthToken.id == token_id)
        query_result = await self._session.execute(statement)
        return AuthTokenMapper.to_domain(query_result.scalar_one_or_none())

    async def find_all_refresh_tokens_by_user_id(self, user_id: uuid.UUID) -> list[AuthTokenAggregate]:
        statement = (
            select(AuthToken)
            .where(
                AuthToken.user_id == user_id,
                AuthToken.token_type == TokenTypeEnum.REFRESH_TOKEN,
                AuthToken.is_revoked == False
            )
        )

        query_result = await self._session.execute(statement)
        orm_tokens = query_result.scalars().all()
        return [AuthTokenMapper.to_domain(token) for token in orm_tokens]

    async def save(self, token_aggregate: AuthTokenAggregate) -> None:
        token_model = AuthTokenMapper.to_orm(token_aggregate)
        await self._session.merge(token_model)
        await self._session.flush()
