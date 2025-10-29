import asyncio

from src.api.auth.auth_dto import ForgotPasswordDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.shared.application.abstract_uow import AbstractUserIdentityUnitOfWork
from src.core.shared.infrastructure.services.email_sender import AbstractEmailSender


class ForgotPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserIdentityUnitOfWork,
        token_service: AbstractTokenService,
        email_sender: AbstractEmailSender
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.email_sender = email_sender

    async def execute(self, forgot_password_dto: ForgotPasswordDTO):
        async with self.unit_of_work as uow:
            user = await uow.user.get_by_user_email(forgot_password_dto.email)
            if not user:
                await asyncio.sleep(0.5)
                return

            token = self.token_service.create_auth_token(user.id, TokenTypeEnum.PASSWORD_RESET_TOKEN)
            identity = await uow.identity.get_user_identity(user.id)

            identity.add_new_token(
                token_type=token.token_type,
                token_value=token.token_value,
                expires_at=token.expires_at
            )

            await uow.identity.save(identity)
            await uow.commit()

        await self.email_sender.send_password_reset_confirmation(
            to_email=user.email,
            template_data={
                "reset_password_token": token.token_value
            }
        )