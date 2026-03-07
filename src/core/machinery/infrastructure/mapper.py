from src.core.machinery.domain.value_objects import Title, Price, YearOfIssue
from src.core.machinery.infrastructure.models import Machinery as ORMMachinery
from src.core.machinery.domain.entities import Machinery as DomainMachinery


class MachineryMapper:
    @staticmethod
    def to_domain(orm_model: ORMMachinery) -> DomainMachinery:
        return DomainMachinery(
            id=orm_model.id,
            customer_id=orm_model.customer_id,
            subcategory_id=orm_model.subcategory_id,
            title=Title(orm_model.title),
            price=Price(orm_model.price),
            currency=orm_model.currency,
            city_id=orm_model.city_id,
            description=orm_model.description,
            brand_id=orm_model.brand_id,
            model=orm_model.model,
            year_of_issue=YearOfIssue(orm_model.year_of_issue),
            condition=orm_model.condition,
            color_id=orm_model.color_id,
            attributes=orm_model.attributes,
            country_id=orm_model.country_id,
            status=orm_model.status,
        )

    @staticmethod
    def to_orm(domain_model: DomainMachinery) -> ORMMachinery:
        return ORMMachinery(
            id=domain_model.id,
            customer_id=domain_model.customer_id,
            subcategory_id=domain_model.subcategory_id,
            title=domain_model.title.value,
            price=domain_model.price.value,
            currency=domain_model.currency,
            city_id=domain_model.city_id,
            description=domain_model.description,
            brand_id=domain_model.brand_id,
            model=domain_model.model,
            year_of_issue=domain_model.year_of_issue.value,
            condition=domain_model.condition,
            color_id=domain_model.color_id,
            attributes=domain_model.attributes,
            country_id=domain_model.country_id,
            status=domain_model.status,
        )
