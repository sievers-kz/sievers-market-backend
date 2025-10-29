from src.api.users.user_dto import EmailConfirmationDTO
from src.core.shared.application.abstract_uow import AbstractUserIdentityUnitOfWork
from src.core.users.domain.exceptions.exception_classes import InvalidEmailConfirmationCodeError


class EmailConfirmationUseCase:
    def __init__(self, unit_of_work: AbstractUserIdentityUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, confirmation_data: EmailConfirmationDTO):
        async with self.unit_of_work as uow:
            identity = await uow.identity.find_by_token_value(confirmation_data.confirmation_code)
            if not identity:
                raise InvalidEmailConfirmationCodeError(code="invalid_confirmation_code")

            user = await uow.user.get_user_by_id(identity.user_id)
            user.confirm_user()
            await uow.user.save(user)

            identity.revoke_token(confirmation_data.confirmation_code)
            await uow.identity.save(identity)
            await uow.commit()
