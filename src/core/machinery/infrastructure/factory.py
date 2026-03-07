import uuid
from uuid import UUID

from src.core.machinery.domain.entities import Machinery
from src.core.machinery.domain.value_objects import Title, Price, YearOfIssue
from src.core.shared.domain.enums import ListingStatus, PriceCurrency
from src.core.machinery.domain.enums import MachineryCondition


class MachineryFactory:
    @staticmethod
    def create(
        customer_id: UUID,
        subcategory_id: UUID,
        title: str,
        price: int,
        currency: PriceCurrency,
        city_id: UUID,
        description: str | None,
        brand_id: UUID,
        model: str | None,
        year_of_issue: int,
        condition: MachineryCondition,
        color_id: UUID | None,
        attributes: dict,
        country_id: UUID | None,
        **kwargs
    ) -> Machinery:
        return Machinery(
            id=uuid.uuid4(),
            customer_id=customer_id,
            subcategory_id=subcategory_id,
            title=Title(title),
            price=Price(price),
            currency=currency,
            city_id=city_id,
            description=description,
            brand_id=brand_id,
            model=model,
            year_of_issue=YearOfIssue(year_of_issue),
            condition=condition,
            color_id=color_id,
            attributes=attributes,
            country_id=country_id,
            status=ListingStatus.ACTIVE,
        )