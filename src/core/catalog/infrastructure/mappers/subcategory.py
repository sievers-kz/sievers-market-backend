from src.core.catalog.domain.entities import Subcategory as DomainSubcategory
from src.core.catalog.domain.value_objects import Attribute
from src.core.catalog.infrastructure.models import Subcategory as ORMSubcategory


class SubcategoryMapper:
    @staticmethod
    def to_orm(domain_model: DomainSubcategory) -> ORMSubcategory:
        return ORMSubcategory(
            id=domain_model.id,
            category_id=domain_model.category_id,
            name=domain_model.name,
            attributes=[attr.to_dict() for attr in domain_model.attributes],
            status=domain_model.status,
        )

    @staticmethod
    def to_domain(orm_model: ORMSubcategory) -> DomainSubcategory:
        return DomainSubcategory(
            id=orm_model.id,
            category_id=orm_model.category_id,
            name=orm_model.name,
            attributes=[Attribute.from_dict(attr) for attr in orm_model.attributes],
            status=orm_model.status,
        )
