from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer
from src.core.users.domain.value_objects import Email, Phone, Fullname, OrganizationFullname, DocumentValue

from src.core.users.infrastructure.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    BusinessDetails as BusinessDetailsModel
)

from src.core.users.domain.entities import (
    User as DomainUser,
    UserProfile as DomainUserProfile,
    BusinessDetails as DomainBusinessDetails
)


class UserMapper:
    @staticmethod
    def to_domain(orm_model: UserModel) -> DomainUser:
        profile = _UserProfileMapper.to_domain(orm_model.profile)

        if orm_model.business_details is not None:
            business_details = _BusinessDetailsMapper.to_domain(orm_model.business_details)
        else:
            business_details = None

        return DomainUser(
            id=orm_model.id,
            role=orm_model.role,
            email=Email.from_raw(orm_model.email),
            phone=Phone.from_raw(PhoneNormalizer.normalize(orm_model.phone)),
            is_active=orm_model.is_active,
            profile=profile,
            business_details=business_details
        )

    @staticmethod
    def to_orm(domain_model: DomainUser) -> UserModel:
        profile = _UserProfileMapper.to_orm(domain_model.profile)

        if domain_model.business_details is not None:
            business_details = _BusinessDetailsMapper.to_orm(domain_model.business_details)
        else:
            business_details = None

        return UserModel(
            id=domain_model.id,
            role=domain_model.role,
            email=domain_model.email.value,
            phone=domain_model.phone.value,
            is_active=domain_model.is_active,
            profile=profile,
            business_details=business_details
        )


class _UserProfileMapper:
    @staticmethod
    def to_domain(orm_model: UserProfileModel) -> DomainUserProfile:
        return DomainUserProfile(
            id=orm_model.id,
            user_id=orm_model.user_id,
            fullname=Fullname.from_raw(
                first_name=orm_model.first_name,
                last_name=orm_model.last_name,
                patronymic=orm_model.patronymic
            ),
            avatar_url=orm_model.avatar_url,
        )

    @staticmethod
    def to_orm(domain_model: DomainUserProfile) -> UserProfileModel:
        return UserProfileModel(
            id=domain_model.id,
            user_id=domain_model.user_id,
            first_name=domain_model.fullname.first_name,
            last_name=domain_model.fullname.last_name,
            patronymic=domain_model.fullname.patronymic,
            avatar_url=domain_model.avatar_url,
        )


class _BusinessDetailsMapper:
    @staticmethod
    def to_domain(orm_model: BusinessDetailsModel) -> DomainBusinessDetails:
        return DomainBusinessDetails(
            id=orm_model.id,
            user_id=orm_model.user_id,
            business_type=orm_model.business_type,
            organization_fullname=OrganizationFullname.from_raw(orm_model.organization_fullname),
            document_type=orm_model.document_type,
            document_value=DocumentValue.from_raw(orm_model.document_value)
        )

    @staticmethod
    def to_orm(domain_model: DomainBusinessDetails) -> BusinessDetailsModel:
        return BusinessDetailsModel(
            id=domain_model.id,
            user_id=domain_model.user_id,
            business_type=domain_model.business_type,
            organization_fullname=domain_model.organization_fullname.value,
            document_type=domain_model.document_type,
            document_value=domain_model.document_value.value
        )