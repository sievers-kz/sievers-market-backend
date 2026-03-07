import asyncio

from src.api.iam.dto import ForgotPasswordData
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.interfaces.abstract_account_notifier import AbstractAccountNotifier
from src.core.iam.domain.enums import TokenType
from src.core.iam.infrastructure.services.pyjwt_token import AbstractTokenService


class ForgotPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        token_service: AbstractTokenService,
        notifier: AbstractAccountNotifier
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.notifier = notifier

    async def execute(self, forgot_password_data: ForgotPasswordData):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(forgot_password_data.email)
            if not account:
                await asyncio.sleep(0.5)
                return

            password_token = self.token_service.create_token(account.id, TokenType.PASSWORD)
            account.request_reset_password(password_token.value, password_token.expires_at)

            await uow.account.save(account)
            await uow.commit()

            await self.notifier.send_password_recovery(
                destination=account.email.value,
                code=password_token.value
            )
