from src.core.machinery.infrastructure.models import Machinery as ORMMachinery
from src.core.machinery.domain.entities import Machinery as DomainMachinery


class MachineryMapper:
    @staticmethod
    def to_domain(orm_model: ORMMachinery) -> DomainMachinery:
        return DomainMachinery(
            id=orm_model.id,
            seller_id=orm_model.seller_id,
            subcategory_id=orm_model.subcategory_id,
            title=orm_model.title,
            price=orm_model.price,
            currency=orm_model.currency,
            city_id=orm_model.city_id,
            description=orm_model.description,
            brand_id=orm_model.brand_id,
            model=orm_model.model,
            year_of_issue=orm_model.year_of_issue,
            condition=orm_model.condition,
            color_id=orm_model.color_id,
            attributes=orm_model.attributes,
            country_id=orm_model.country_id,
            status=orm_model.status,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
        )

    @staticmethod
    def to_orm(domain_model: DomainMachinery) -> ORMMachinery:
        return ORMMachinery(
            id=domain_model.id,
            seller_id=domain_model.seller_id,
            subcategory_id=domain_model.subcategory_id,
            title=domain_model.title,
            price=domain_model.price,
            currency=domain_model.currency,
            city_id=domain_model.city_id,
            description=domain_model.description,
            brand_id=domain_model.brand_id,
            model=domain_model.model,
            year_of_issue=domain_model.year_of_issue,
            condition=domain_model.condition,
            color_id=domain_model.color_id,
            attributes=domain_model.attributes,
            country_id=domain_model.country_id,
            status=domain_model.status,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at,
        )
