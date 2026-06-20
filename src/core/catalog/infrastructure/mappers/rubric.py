from src.core.catalog.domain.entities import Rubric as DomainRubric
from src.core.catalog.domain.value_objects import Attribute
from src.core.catalog.infrastructure.models import Rubric as ORMRubric


class RubricMapper:
    @staticmethod
    def to_orm(domain_model: DomainRubric) -> DomainRubric:
        return ORMRubric(
            id=domain_model.id,
            name=domain_model.name,
            attributes=[attr.to_dict() for attr in domain_model.attributes],
            status=domain_model.status,
        )

    @staticmethod
    def to_domain(orm_model: ORMRubric) -> DomainRubric:
        return DomainRubric(
            id=orm_model.id,
            name=orm_model.name,
            attributes=[Attribute.from_dict(attr) for attr in orm_model.attributes],
            status=orm_model.status,
        )
