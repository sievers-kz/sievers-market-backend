import uuid

from src.api.users.user_dto import DocumentValueDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.users.application.abstract_user_uow import AbstractUserUnitOfWork


class ChangeDocumentValueUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        token_service: AbstractTokenService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, document_value_dto: DocumentValueDTO):
        payload = self.token_service.verify_token(document_value_dto.access_token, TokenTypeEnum.ACCESS_TOKEN)
        user_id = uuid.UUID(payload.get("sub"))

        async with self.unit_of_work as uow:
            user = await uow.user.get_user_by_id(user_id)
            user.change_business_details_document_value(document_value_dto.document_value)

            await uow.user.save(user)
            await uow.commit()

