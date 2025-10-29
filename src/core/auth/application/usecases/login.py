from src.api.auth.auth_dto import LoginUserDTO, LoginResponseDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import InvalidCredentialsError
from src.core.auth.infrastructure.factories import UserIdentityFactory
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.shared.application.abstract_uow import AbstractUserIdentityUnitOfWork


class LoginUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserIdentityUnitOfWork,
        token_service: AbstractTokenService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, login_data: LoginUserDTO):
        async with self.unit_of_work as uow:
            user = await uow.user.get_by_user_email(login_data.email)
            if not user:
                raise InvalidCredentialsError(code="invalid_credentials_error")

            identity = await uow.identity.get_user_identity(user.id)
            identity.password_is_matches(login_data.raw_password)

            access_token = self.token_service.create_auth_token(user_id=user.id, token_type=TokenTypeEnum.ACCESS_TOKEN)
            refresh_token = self.token_service.create_auth_token(user_id=user.id, token_type=TokenTypeEnum.REFRESH_TOKEN)

            identity.add_new_token(
                token_type=refresh_token.token_type,
                token_value=refresh_token.token_value,
                expires_at=refresh_token.expires_at
            )

            await uow.identity.save(identity)
            await uow.commit()

        return LoginResponseDTO(
            access_token=access_token.token_value,
            refresh_token=refresh_token.token_value
        )
