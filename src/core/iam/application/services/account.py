import uuid
from uuid import UUID

from src.core.iam.application.interfaces.abstract_account_repository import AbstractAccountRepository
from src.core.iam.application.interfaces.abstract_factory import AbstractAccountFactory
from src.core.iam.application.interfaces.abstract_token_service import AbstractTokenService
from src.core.iam.domain.enums import TokenType


class AccountService:
    def __init__(self, repository: AbstractAccountRepository, token_service: AbstractTokenService, factory: AbstractAccountFactory):
        self.repository = repository
        self.token_service = token_service
        self.factory = factory

    async def create(self, email: str, raw_password: str) -> UUID:
        account_id = uuid.uuid4()
        token = self.token_service.create_token(account_id, TokenType.EMAIL)
        account = self.factory.create(account_id=account_id, email=email, raw_password=raw_password, token_data=[token])
        await self.repository.save(account)
        return account_id
