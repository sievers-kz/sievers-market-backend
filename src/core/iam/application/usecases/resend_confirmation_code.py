import asyncio

from src.api.iam.dto import ResendCodeRequest
from src.core.iam.application.interfaces.abstract_account_confirmation import AbstractAccountConfirmation
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.interfaces.abstract_token_service import AbstractTokenService
from src.core.iam.domain.enums import TokenType


class ResendConfirmationCodeUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        token_service: AbstractTokenService,
        notifier: AbstractAccountConfirmation
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.notifier = notifier

    async def execute(self, resend_data: ResendCodeRequest):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(resend_data.email)
            if not account:
                await asyncio.sleep(0.5)
                return

            email_token = self.token_service.create_token(account.id, TokenType.EMAIL, account.role)
            account.resend_confirmation_code(email_token.value, email_token.expires_at)

            await uow.account.save(account)
            await uow.commit()

            await self.notifier.send_confirmation_code(
                destination=account.email.value,
                code=email_token.value
            )
