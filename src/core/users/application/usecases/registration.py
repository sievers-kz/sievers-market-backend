from src.api.users.user_dto import UserDTO, TokenDataDTO
from src.core.users.application.exceptions.exception_classes import InternalServerError, ServiceUnavailableError
from src.core.users.application.uow import AbstractUserUnitOfWork
from src.core.users.domain.entities import UserAggregate
from src.core.users.domain.exceptions.exception_classes import UserAlreadyExistsError

from src.core.users.infrastructure.exceptions.exception_classes import (
    UniqueConstraintError,
    RepositoryError,
    TokenGeneratorService,
    UnitOfWorkError,
    DatabaseConnectionError,
    EmailSenderError
)

from src.core.users.infrastructure.factories import UserFactory, AuthTokenFactory
from src.core.users.infrastructure.services.email_sender import AbstractEmailSender
from src.core.users.infrastructure.services.pyjwt_token import PyJWTTokenService


class RegisterUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        email_sender: AbstractEmailSender,
        token_service: PyJWTTokenService # FIXME: Use some abstraction interface (AbstractTokenService)
    ):
        self.unit_of_work = unit_of_work
        self.email_sender = email_sender
        self.token_service = token_service

    async def execute(self, user_dto: UserDTO):
        try:
            async with self.unit_of_work as uow:
                user = UserFactory.create(user_dto)
                await uow.user.save(user)

                token_aggregate, email_token = await self._create_confirmation_token(user)
                await uow.token.save(token_aggregate)

                await uow.commit()
                await self._send_email_confirmation(user, email_token)

        except UniqueConstraintError as exc:
            raise UserAlreadyExistsError(
                code="user_already_exists",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

        except (RepositoryError, TokenGeneratorService) as exc:
            raise InternalServerError(
                code="internal_server_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

        except (UnitOfWorkError, DatabaseConnectionError) as exc:
            raise ServiceUnavailableError(
                code="service_unavailable_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

    async def _create_confirmation_token(self, user):
        email_token = self.token_service.create_email_token(user.id)
        token_aggregate = AuthTokenFactory.create_email_token(
            user_id=user.id,
            expires_at=email_token.expires_at,
            token_value=email_token.token_str
        )
        return token_aggregate, email_token

    async def _send_email_confirmation(self, user: UserAggregate, email_token: TokenDataDTO):
        try:
            await self.email_sender.send_email_confirmation(
                to_email=user.email.value,
                template_data={
                    "confirmation_token": email_token.token_str,
                    "first_name": user.fullname.first_name
                }
            )

        except EmailSenderError as exc:
            raise ServiceUnavailableError(
                code="service_unavailable_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc
