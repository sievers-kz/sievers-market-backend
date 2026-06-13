from src.core.catalog.domain.entities import Category as DomainCategory
from src.core.catalog.infrastructure.models import Category as ORMCategory


class CategoryMapper:
    @staticmethod
    def to_orm(domain_model: DomainCategory) -> ORMCategory:
        return ORMCategory(
            id=domain_model.id,
            rubric_id=domain_model.rubric_id,
            name=domain_model.name,
            status=domain_model.status,
        )

    @staticmethod
    def to_domain(orm_model: ORMCategory) -> DomainCategory:
        return DomainCategory(
            id=orm_model.id,
            rubric_id=orm_model.rubric_id,
            name=orm_model.name,
            status=orm_model.status,
        )
