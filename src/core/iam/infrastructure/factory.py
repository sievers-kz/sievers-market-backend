import uuid
from datetime import datetime

from src.core.iam.presentation.dto import CreateUserRequest
from src.core.iam.domain.entities import Account
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

    def create(self, data: CreateUserRequest,) -> Account:
        hashed_password = self.password_hasher.hash_password(data.raw_password)

        return Account(
            id=uuid.uuid4(),
            email=Email(data.email),
            phone=Phone(value=None),
            password=Password(hashed_password),
            is_active=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tokens=[]
        )


