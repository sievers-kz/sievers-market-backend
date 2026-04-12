import uuid
from uuid import UUID

from src.core.machinery.domain.entities import Machinery
from src.core.machinery.domain.value_objects import Title, Price, YearOfIssue, Description
from src.core.machinery.presentation.dto import CreateMachineryRequest
from src.core.shared.domain.enums import ListingStatus, PriceCurrency
from src.core.machinery.domain.enums import MachineryCondition


class MachineryFactory:
    @staticmethod
    def create(
        customer_id: UUID,
        title: Title,
        attibutes: dict,
        dto: CreateMachineryRequest
    ) -> Machinery:
        return Machinery(
            id=uuid.uuid4(),
            customer_id=customer_id,
            subcategory_id=dto.subcategory_id,
            title=title,
            price=Price(dto.price),
            currency=dto.currency,
            city_id=dto.city_id,
            description=Description(dto.description),
            brand_id=dto.brand_id,
            model=dto.model,
            year_of_issue=YearOfIssue(dto.year_of_issue),
            condition=dto.condition,
            color_id=dto.color_id,
            attributes=attibutes,
            country_id=dto.country_id,
            status=ListingStatus.ACTIVE,
        )
