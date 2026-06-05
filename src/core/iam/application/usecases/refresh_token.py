from src.core.iam.presentation.dto import RefreshData, LoginResponse
from src.core.iam.application.interfaces.uow import IIAMUnitOfWork
from src.core.iam.domain.enums import TokenType
from src.core.iam.infrastructure.services.pyjwt_token import ITokenService


class RefreshTokenUseCase:
    def __init__(
        self,
        unit_of_work: IIAMUnitOfWork,
        token_service: ITokenService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, refresh_data: RefreshData):
        try:
            self.token_service.verify_token(refresh_data.refresh_token, TokenType.REFRESH)
        except Exception:
            raise ValueError("Invalid refresh token")

        async with self.unit_of_work as uow:
            account = await uow.account.find_by_token_value(refresh_data.refresh_token)
            if not account:
                raise ValueError("Token not found")

            new_access_token = self.token_service.create_token(account.id, TokenType.ACCESS)
            new_refresh_token = self.token_service.create_token(account.id, TokenType.REFRESH)

            account.rotate_refresh_token(
                refresh_data.refresh_token,
                new_refresh_token.value,
                new_refresh_token.expires_at
            )

            await uow.account.save(account)
            await uow.commit()

            return LoginResponse(
                access_token=new_access_token.value,
                refresh_token=new_refresh_token.value
            )
