from src.api.iam.dto import LoginAccount, LoginResponse
from src.core.iam.domain.enums import TokenType
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.interfaces.abstract_token_service import AbstractTokenService
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher


class LoginUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        token_service: AbstractTokenService,
        password_hasher: AbstractPasswordHasher
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.password_hasher = password_hasher

    async def execute(self, login_data: LoginAccount):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(login_data.email)
            if not account:
                raise ValueError("Invalid email or password")

            account.login(login_data.raw_password, self.password_hasher)

            access_token = self.token_service.create_token(account.id, TokenType.ACCESS)
            refresh_token = self.token_service.create_token(account.id, TokenType.REFRESH)
            account.add_new_token(refresh_token.type, refresh_token.value, refresh_token.expires_at)

            await uow.account.save(account)
            await uow.commit()

            return LoginResponse(access_token=access_token.value, refresh_token=refresh_token.value)
