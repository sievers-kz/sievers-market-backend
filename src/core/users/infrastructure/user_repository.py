import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.users.domain.entities import UserAggregate
from src.core.users.domain.interfaces import AbstractRepository
from src.core.users.infrastructure.exceptions.exception_classes import UniqueConstraintError, RepositoryError
from src.core.users.infrastructure.mappers import UserMapper
from src.configuration.database.models.users import User


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


