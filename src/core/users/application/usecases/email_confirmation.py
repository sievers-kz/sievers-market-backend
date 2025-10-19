from src.api.users.user_dto import EmailConfirmationDTO
from src.core.auth.application.exceptions.exception_classes import ServiceUnavailableError, InternalServerError
from src.core.shared.application.abstract_uow import AbstractUserAuthUnitOfWork

from src.core.users.domain.exceptions.exception_classes import (
    InvalidEmailConfirmationCodeError,
    ConfirmationCodeExpiredError
)

from src.core.auth.infrastructure.exceptions.exception_classes import RepositoryError
from src.core.shared.infrastructure.exceptions.exception_classes import DatabaseConnectionError, UnitOfWorkError


class EmailConfirmationUseCase:
    def __init__(self, unit_of_work: AbstractUserAuthUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, confirmation_data: EmailConfirmationDTO):
        try:
            async with self.unit_of_work as uow:
                token = await self._validate_confirmation_token(confirmation_data, uow)

                user = await uow.user.get_by_id(token.user_id)
                user.confirm_email()
                await uow.user.save(user)

                token.revoke_token()
                await uow.token.save(token)
                await uow.commit()

        except RepositoryError as exc:
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

    async def _validate_confirmation_token(
            self,
            confirmation_data: EmailConfirmationDTO,
            uow: AbstractUserAuthUnitOfWork
    ):
        token = await uow.token.find_by_value(confirmation_data.confirmation_code)
        if not token:
            raise InvalidEmailConfirmationCodeError(code="invalid_confirmation_code")

        if token.is_expired():
            raise ConfirmationCodeExpiredError(code="confirmation_code_expired")

        return token
