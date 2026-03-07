from datetime import datetime
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field, ConfigDict

from src.core.machinery.infrastructure.models import Machinery
from src.core.shared.domain.enums import ListingStatus


class MachineryFilter(Filter):
    subcategory_id: UUID | None = Field(None, alias="subcategory_id")
    city_id: UUID | None = Field(None, alias="city_id")

    price__gte: int | None = Field(None, alias="min_price")
    price__lte: int | None = Field(None, alias="max_price")

    year_of_issue__gte: int | None = Field(None, alias="min_year_of_issue")
    year_of_issue__lte: int | None = Field(None, alias="max_year_of_issue")

    engine_power__gte: int | None = Field(None, alias="min_engine_power")
    engine_power__lte: int | None = Field(None, alias="max_engine_power")

    weight__gte: int | None = Field(None, alias="min_weight_gte")
    weight__lte: int | None = Field(None, alias="max_weight_lte")

    length__gte: int | None = Field(None, alias="min_length")
    length__lte: int | None = Field(None, alias="max_length")

    width__gte: int | None = Field(None, alias="min_width")
    width__lte: int | None = Field(None, alias="max_width")

    height__gte: int | None = Field(None, alias="min_height")
    height__lte: int | None = Field(None, alias="max_height")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )

    class Constants(Filter.Constants):
        model = Machinery


class MachineryOwnerFilter(Filter):
    status: ListingStatus | None = Field(ListingStatus.ACTIVE, alias="listing_status")
    created_at__gte: datetime | None = Field(None, alias="created_at_min")
    created_at__lte: datetime | None = Field(None, alias="created_at_max")

    class Constants(Filter.Constants):
        model = Machinery
