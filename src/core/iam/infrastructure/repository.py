from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.iam.application.interfaces.abstract_account_repository import AbstractAccountRepository
from src.core.iam.infrastructure.mapper import AccountMapper
from src.core.iam.infrastructure.models import Account as ORMAccount, Token as ORMToken
from src.core.iam.domain.entities import Account as DomainAccount


class AccountRepository(AbstractAccountRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._model = ORMAccount
        self._token_model = ORMToken

    async def save(self, account: DomainAccount):
        mapped_model = AccountMapper.to_orm(account)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_account_by_id(self, account_id: UUID) -> DomainAccount:
        statement = (
            select(self._model)
            .options(selectinload(self._model.tokens))
            .where(self._model.id == account_id)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.unique().scalar_one_or_none()

        if orm_model is None:
            return None

        return AccountMapper.to_domain(orm_model)

    async def find_by_token_value(self, token_value: str) -> DomainAccount:
        statement = (
            select(self._model)
            .join(self._token_model, self._model.id == self._token_model.account_id)
            .where(self._token_model.value == token_value)
            .options(
                selectinload(self._model.tokens)
            )
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.unique().scalar_one_or_none()

        if orm_model is None:
            return None

        return AccountMapper.to_domain(orm_model)

    async def get_account_by_email(self, email: str) -> DomainAccount:
        statement = (
            select(self._model)
            .options(selectinload(self._model.tokens))
            .where(self._model.email == email)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.unique().scalar_one_or_none()

        if orm_model is None:
            return None

        return AccountMapper.to_domain(orm_model)
