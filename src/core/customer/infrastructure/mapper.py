from src.core.customer.domain.entities import Customer as DomainCustomer
from src.core.customer.domain.entities import Organization as DomainOrganization
from src.core.customer.domain.value_objects import Fullname
from src.core.customer.infrastructure.models import Customer as ORMCustomer
from src.core.customer.infrastructure.models import Organization as ORMOrganization


class CustomerMapper:
    @staticmethod
    def to_orm(customer: DomainCustomer) -> ORMCustomer:
        return ORMCustomer(
            id=customer.id,
            account_id=customer.account_id,
            last_name=customer.fullname.last_name,
            first_name=customer.fullname.first_name,
            patronymic=customer.fullname.patronymic,
        )

    @staticmethod
    def to_domain(customer: ORMCustomer) -> DomainCustomer:
        return DomainCustomer(
            id=customer.id,
            account_id=customer.account_id,
            fullname=Fullname(
                last_name=customer.last_name,
                first_name=customer.first_name,
                patronymic=customer.patronymic,
            ),
        )


class OrganizationMapper:
    @staticmethod
    def to_orm(organization: DomainOrganization) -> ORMOrganization:
        return ORMOrganization(
            id=organization.id,
            owner_id=organization.owner_id,
            legal_name=organization.legal_name,
            legal_address=organization.legal_address,
            tax_id=organization.tax_id,
            kind=organization.kind,
            form=organization.form,
            shop_name=organization.shop_name,
            logo_media_id=organization.logo_media_id,
            is_registry_verified=organization.is_registry_verified,
            is_ownership_verified=organization.is_ownership_verified,
            contact_phone=organization.contact_phone,
            contact_email=organization.contact_email,
        )

    @staticmethod
    def to_domain(organization: ORMOrganization) -> DomainOrganization:
        return DomainOrganization(
            id=organization.id,
            owner_id=organization.owner_id,
            legal_name=organization.legal_name,
            legal_address=organization.legal_address,
            tax_id=organization.tax_id,
            kind=organization.kind,
            form=organization.form,
            shop_name=organization.shop_name,
            logo_media_id=organization.logo_media_id,
            is_registry_verified=organization.is_registry_verified,
            is_ownership_verified=organization.is_ownership_verified,
            contact_phone=organization.contact_phone,
            contact_email=organization.contact_email,
        )
