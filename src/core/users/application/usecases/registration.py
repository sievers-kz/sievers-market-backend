from src.api.users.user_dto import CreateUserDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.factories import UserIdentityFactory
from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.shared.application.abstract_uow import AbstractUserIdentityUnitOfWork
from src.core.shared.infrastructure.services.email_sender import AbstractEmailSender
from src.core.users.domain.enums import UserRoleEnum
from src.core.users.infrastructure.factories import UserFactory


class CreateUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserIdentityUnitOfWork,
        email_sender: AbstractEmailSender,
        token_service: PyJWTTokenService
    ):
        self.unit_of_work = unit_of_work
        self.email_sender = email_sender
        self.token_service = token_service

    async def execute(self, user_data: CreateUserDTO):
        async with self.unit_of_work as uow:
            if user_data.role == UserRoleEnum.INDIVIDUAL:
                user = UserFactory.create_individual_user(user_data)
            else:
                user = UserFactory.create_business_user(user_data)
            await uow.user.save(user)

            credentials = user_data.credentials
            tokens = self.token_service.create_auth_token(user_id=user.id, token_type=TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN)
            identity = UserIdentityFactory.create(user_id=user.id, credentials=credentials, tokens=[tokens])

            await uow.identity.save(identity)
            await uow.commit()

        await self.email_sender.send_email_confirmation(
            to_email=user.email.value,
            template_data={
                "confirmation_token": tokens.token_value
            }
        )
