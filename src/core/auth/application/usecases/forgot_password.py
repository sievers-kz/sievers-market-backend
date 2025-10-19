import asyncio

from src.api.users.user_dto import TokenDataDTO
from src.api.auth.auth_dto import ForgotPasswordDTO
from src.core.auth.application.exceptions.exception_classes import InternalServerError, ServiceUnavailableError
from src.core.shared.application.abstract_uow import AbstractUserAuthUnitOfWork
from src.core.users.domain.entities import UserAggregate
from src.core.auth.domain.entities import AuthTokenAggregate

from src.core.shared.infrastructure.exceptions.exception_classes import DatabaseConnectionError, UnitOfWorkError
from src.core.auth.infrastructure.exceptions.exception_classes import RepositoryError, TokenGeneratorService

from src.core.shared.infrastructure.exceptions.exception_classes import EmailSenderError
from src.core.auth.infrastructure.factories import AuthTokenFactory
from src.core.shared.infrastructure.services.email_sender import AbstractEmailSender
from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService


class ForgotPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserAuthUnitOfWork,
        token_service: PyJWTTokenService,
        email_sender: AbstractEmailSender
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.email_sender = email_sender

    async def execute(self, forgot_password_dto: ForgotPasswordDTO):
        try:
            async with self.unit_of_work as uow:
                user = await uow.user.get_by_email(forgot_password_dto.email)
                if not user:
                    await asyncio.sleep(0.5)
                    return

                token = self.token_service.create_password_reset_token(user.id)
                token_aggregate = self._persist_token_aggregate(user, token)
                await uow.token.save(token_aggregate)

                await uow.commit()
            await self._send_reset_password_message(user, token_aggregate)

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

    def _persist_token_aggregate(self, user: UserAggregate, token: TokenDataDTO):
        return AuthTokenFactory.create_password_reset_token(
            user_id=user.id,
            token_value=token.token_str,
            expires_at=token.expires_at
        )

    async def _send_reset_password_message(self, user: UserAggregate, token_aggregate: AuthTokenAggregate):
        try:
            await self.email_sender.send_password_reset_confirmation(
                to_email=user.email.value,
                template_data={
                    "reset_password_token": token_aggregate.token_value,
                    "first_name": user.fullname.first_name
                }
            )

        except EmailSenderError as exc:
            raise ServiceUnavailableError(
                code="service_unavailable_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc
