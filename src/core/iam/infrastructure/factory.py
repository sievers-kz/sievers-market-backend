from datetime import datetime
from uuid import UUID

from src.api.iam.dto import TokenData, CreateUserRequest
from src.core.iam.domain.entities import Account, Token
from src.core.iam.domain.value_objects import Password
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher
from src.core.shared.infrastructure.services.phone_normalizer import AbstractPhoneNormalizer
from src.core.iam.domain.value_objects import Email, Phone


class AccountFactory:
    def __init__(
        self,
        phone_normalizer: AbstractPhoneNormalizer,
        password_hasher: AbstractPasswordHasher
    ):
        self.phone_normalizer = phone_normalizer
        self.password_hasher = password_hasher

    def create(
        self,
        account_id: UUID,
        account_data: CreateUserRequest,
        token_data: list[TokenData]
    ) -> Account:

        hashed_password = self.password_hasher.hash_password(account_data.raw_password)
        tokens = [Token.create(account_id, token.type, token.value, token.expires_at) for token in token_data]

        return Account(
            id=account_id,
            email=Email(account_data.email),
            phone=Phone(value=None),
            password=Password(hashed_password),
            is_active=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tokens=tokens
        )


