import uuid

from src.api.users.user_dto import UserProfileDTO, BusinessDetailsDTO, CreateUserDTO
from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer

from src.core.users.domain.entities import (
    User as DomainUser,
    UserProfile as DomainUserProfile,
    BusinessDetails as DomainBusinessDetails
)
from src.core.users.domain.enums import UserRoleEnum

from src.core.users.domain.value_objects import Email, Phone, Fullname, OrganizationFullname, DocumentValue


class UserFactory:
    @staticmethod
    def create(dto: CreateUserDTO):
        user_id = uuid.uuid4()
        profile = _UserProfileFactory.create(dto.profile, user_id)

        business_details = None
        if dto.role == UserRoleEnum.BUSINESS and dto.business_details:
            business_details = _BusinessDetailsFactory.create(dto.business_details, user_id)

        return DomainUser(
            id=user_id,
            role=dto.role,
            email=Email.from_raw(dto.email),
            phone=Phone.from_raw(PhoneNormalizer.normalize(dto.phone)),
            is_active=False,
            profile=profile,
            business_details=business_details
        )


class _UserProfileFactory:
    @staticmethod
    def create(dto: UserProfileDTO, user_id: uuid.UUID) -> DomainUserProfile:
        return DomainUserProfile(
            id=user_id,
            user_id=user_id,
            fullname=Fullname.from_raw(
                first_name=dto.first_name,
                last_name=dto.last_name,
                patronymic=dto.patronymic
            ),
            avatar_url=dto.avatar_url
        )


class _BusinessDetailsFactory:
    @staticmethod
    def create(dto: BusinessDetailsDTO, user_id: uuid.UUID) -> DomainBusinessDetails:
        return DomainBusinessDetails(
            id=uuid.uuid4(),
            user_id=user_id,
            business_type=dto.business_type,
            organization_fullname=OrganizationFullname.from_raw(dto.organization_fullname),
            document_type=dto.document_type,
            document_value=DocumentValue.from_raw(raw_value=dto.document_value)
        )