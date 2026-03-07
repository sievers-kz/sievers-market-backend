import uuid

from src.api.iam.dto import CreateUserRequest
from src.core.iam.application.interfaces.abstract_factory import AbstractAccountFactory
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.interfaces.abstract_account_notifier import AbstractAccountNotifier
from src.core.iam.application.interfaces.abstract_profile_creator import AbstractProfileCreator
from src.core.iam.domain.entities import Account
from src.core.iam.domain.enums import TokenType
from src.core.iam.application.interfaces.abstract_token_service import AbstractTokenService


class CreateUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        token_service: AbstractTokenService,
        factory: AbstractAccountFactory,
        profile_creator: AbstractProfileCreator,
        notifier: AbstractAccountNotifier
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.factory = factory
        self.profile_creator = profile_creator
        self.notifier = notifier

    async def execute(self, dto: CreateUserRequest):
        async with self.unit_of_work as uow:
            account_id = uuid.uuid4()
            email_token = self.token_service.create_token(account_id, TokenType.EMAIL)

            account: Account = self.factory.create(account_id, dto, [email_token])
            await uow.account.save(account)

            await self.profile_creator.create(account_id, dto.last_name, dto.first_name)
            await uow.commit()

            await self.notifier.send_confirmation_code(
                destination=account.email.value,
                code=email_token.value
            )
