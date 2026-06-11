from src.core.vendor.domain.value_objects import Logotype, TaxID, ContactFullname
from src.core.vendor.infrastructure.models import Vendor as ORMVendor
from src.core.vendor.domain.entities import Vendor as DomainVendor


class VendorMapper:
    @staticmethod
    def to_orm(domain_model: DomainVendor) -> ORMVendor:
        return ORMVendor(
            id=domain_model.id,
            account_id=domain_model.account_id,
            is_verified=domain_model.is_verified,
            contact_last_name=domain_model.contact_fullname.contact_last_name,
            contact_first_name=domain_model.contact_fullname.contact_first_name,
            contact_patronymic=domain_model.contact_fullname.contact_patronymic,
            contact_phone=domain_model.contact_phone,
            legal_name=domain_model.legal_name,
            legal_address=domain_model.legal_address,
            tax_id=domain_model.tax_id.value,
            legal_form=domain_model.legal_form,
            shop_name=domain_model.shop_name,
            logotype=domain_model.logotype.to_dict() if domain_model.logotype else None,
            status=domain_model.status,
            closed_at=domain_model.closed_at,
        )

    @staticmethod
    def to_domain(orm_model: ORMVendor) -> DomainVendor:
        return DomainVendor(
            id=orm_model.id,
            account_id=orm_model.account_id,
            is_verified=orm_model.is_verified,
            contact_fullname=ContactFullname(
                contact_last_name=orm_model.contact_last_name,
                contact_first_name=orm_model.contact_first_name,
                contact_patronymic=orm_model.contact_patronymic
            ),
            contact_phone=orm_model.contact_phone,
            legal_name=orm_model.legal_name,
            legal_address=orm_model.legal_address,
            tax_id=TaxID(orm_model.tax_id, orm_model.legal_form),
            legal_form=orm_model.legal_form,
            shop_name=orm_model.shop_name,
            logotype=Logotype.from_dict(orm_model.logotype) if orm_model.logotype else None,
            status=orm_model.status,
            closed_at=orm_model.closed_at,
        )
