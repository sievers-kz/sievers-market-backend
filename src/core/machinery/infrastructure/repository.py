import math
from typing import Any
from uuid import UUID

from sqlalchemy import select, inspect, Numeric, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.machinery.dto import MachineryCard, PaginatedMachinery, MachineryOwnerCard, DetailMachinery, SellerInfo, \
    OwnerDetailMachinery
from src.core.iam.infrastructure.models import Account
from src.core.machinery.application.interfaces.abstract_machinery_reader import AbstractMachineryReader
from src.core.machinery.application.interfaces.abstract_machinery_repository import AbstractMachineryRepository
from src.core.machinery.domain.enums import ListingStatus
from src.core.machinery.infrastructure.mapper import MachineryMapper
from src.core.machinery.infrastructure.models import Machinery as ORMMachinery
from src.core.machinery.domain.entities import Machinery as DomainMachinery
from src.core.references.infrastructure.models import Subcategory, City, Brand, Country, Color
from src.core.seller.infrastructure.models import Seller


class MachineryRepository(AbstractMachineryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._machinery = ORMMachinery

    async def save(self, machinery: DomainMachinery) -> None:
        mapped_model = MachineryMapper.to_orm(machinery)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_by_machinery_id(self, machinery_id: UUID) -> DomainMachinery:
        statement = select(self._machinery).where(self._machinery.id == machinery_id)
        query_result = await self._session.execute(statement)

        if not query_result:
            return None

        return MachineryMapper.to_domain(query_result.scalar_one_or_none())


class MachineryReader(AbstractMachineryReader):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._machinery = ORMMachinery

    async def get_seller_machinery(
        self,
        seller_id: UUID,
        status: ListingStatus,
        page: int,
        limit: int
    ):
        statement = (
            select(
                self._machinery.id,
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                self._machinery.status,
                self._machinery.created_at,
                Subcategory.name.label("subcategory"),
                City.name.label("city")
            )
            .select_from(self._machinery)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)
            .where(
                self._machinery.seller_id == seller_id,
                self._machinery.status == status
            )
        )

        count_stmt = select(func.count()).select_from(statement.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        offset = (page - 1) * limit
        paginated_stmt = statement.order_by(self._machinery.created_at.desc()).limit(limit).offset(offset)

        query_result = await self._session.execute(paginated_stmt)
        items = [MachineryOwnerCard(**row) for row in query_result.mappings().all()]
        pages_count = math.ceil(total / limit) if limit > 0 else 0

        return PaginatedMachinery(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages_count=pages_count
        )

    async def get_detail_machinery(self, machinery_id: UUID):
        statement = (
            select(
                self._machinery.id,
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                self._machinery.description,
                self._machinery.model,
                self._machinery.year_of_issue,
                self._machinery.condition,
                self._machinery.attributes,
                Seller.id.label("seller_id"),
                Seller.company_name.label("company_name"),
                Account.phone.label("phone"),
                Subcategory.name.label("subcategory"),
                City.name.label("city"),
                Brand.name.label("brand"),
                Color.name.label("color"),
                Country.name.label("country")
            )
            .join(Seller, self._machinery.seller_id == Seller.id)
            .join(Account, Seller.account_id == Account.id)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)
            .join(Brand, self._machinery.brand_id == Brand.id)
            .join(Color, self._machinery.color_id == Color.id)
            .join(Country, self._machinery.country_id == Country.id)
            .where(
                self._machinery.id == machinery_id,
                self._machinery.status == ListingStatus.ACTIVE
            )
        )

        query_result = await self._session.execute(statement)
        row = query_result.first()
        data = row._asdict()

        return DetailMachinery(
            **data,
            seller=SellerInfo(
                id=data["seller_id"],
                company_name=data["company_name"],
                phone=data["phone"]
            )
        )

    async def get_owner_detail_machinery(self, machinery_id: UUID, seller_id: UUID):
        statement = (
            select(
                self._machinery.id,
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                self._machinery.description,
                self._machinery.model,
                self._machinery.year_of_issue,
                self._machinery.condition,
                self._machinery.status,
                self._machinery.created_at,
                self._machinery.attributes,
                Seller.id.label("seller_id"),
                Seller.company_name.label("company_name"),
                Account.phone.label("phone"),
                Subcategory.name.label("subcategory"),
                City.name.label("city"),
                Brand.name.label("brand"),
                Color.name.label("color"),
                Country.name.label("country")
            )
            .join(Seller, self._machinery.seller_id == Seller.id)
            .join(Account, Seller.account_id == Account.id)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)
            .join(Brand, self._machinery.brand_id == Brand.id)
            .join(Color, self._machinery.color_id == Color.id)
            .join(Country, self._machinery.country_id == Country.id)
            .where(
                self._machinery.id == machinery_id,
                self._machinery.seller_id == seller_id
            )
        )

        query_result = await self._session.execute(statement)
        row = query_result.first()
        data = row._asdict()

        return OwnerDetailMachinery(
            **data,
            seller=SellerInfo(
                id=data["seller_id"],
                company_name=data["company_name"],
                phone=data["phone"]
            )
        )

    async def filter(
        self,
        category_id: UUID | None,
        subcategory_id: UUID | None,
        min_price: int | None,
        max_price: int | None,
        city_id: UUID | None,
        dynamic_filters: dict[str, Any] | None,
        page: int = 1,
        limit: int = 20
    ):
        statement = (
            select(
                self._machinery.id,
                self._machinery.title,
                self._machinery.price,
                self._machinery.currency,
                self._machinery.created_at,
                Subcategory.name.label("subcategory"),
                City.name.label("city")
            )
            .select_from(self._machinery)
            .join(Subcategory, self._machinery.subcategory_id == Subcategory.id)
            .join(City, self._machinery.city_id == City.id)
            .where(self._machinery.status == ListingStatus.ACTIVE)
        )

        filters = []

        if category_id:
            filters.append(Subcategory.category_id == category_id)
        if subcategory_id:
            filters.append(self._machinery.subcategory_id == subcategory_id)
        if min_price:
            filters.append(self._machinery.price >= min_price)
        if max_price:
            filters.append(self._machinery.price <= max_price)
        if city_id:
            filters.append(self._machinery.city_id == city_id)

        if filters:
            statement = statement.where(*filters)

        if dynamic_filters:
            statement = self._apply_dynamic_filters(statement, dynamic_filters)

        count_stmt = select(func.count()).select_from(statement.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        offset = (page - 1) * limit
        paginated_stmt = statement.order_by(self._machinery.created_at.desc()).limit(limit).offset(offset)

        query_result = await self._session.execute(paginated_stmt)
        items = [MachineryCard(**row) for row in query_result.mappings().all()]
        pages_count = math.ceil(total / limit) if limit > 0 else 0

        return PaginatedMachinery(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages_count=pages_count
        )

    def _apply_dynamic_filters(self, statement, filters: dict[str, Any]):
        exclude = {"category_id", "subcategory_id", "min_price", "max_price", "city_id", "page", "limit"}
        model_columns = {column.key for column in inspect(self._machinery).columns}

        for key, raw_value in filters.items():
            if key in exclude or raw_value in [None, ""]:
                continue

            field, operator = self._parse_key(key)

            value = self._cast_value(operator, raw_value)
            if value is None:
                continue

            if field in model_columns:
                column = getattr(self._machinery, field)
                statement = self.filter_by_generated_column(statement, column, operator, value)
            else:
                statement = self.filter_by_jsonb(statement, field, operator, value)

        return statement

    def filter_by_generated_column(self, statement, column: str, operator: str, value: Any):
        if operator == "ge":
            return statement.where(column >= value)
        elif operator == "le":
            return statement.where(column <= value)
        else:
            return statement.where(column == value)

    def filter_by_jsonb(self, statement, field: str, operator: str, value: Any):
        if operator in ["ge", "le"]:
            json_val = self._machinery.attributes[field].astext.cast(Numeric)

            if operator == "ge":
                return statement.where(json_val >= value)
            elif operator == "le":
                return statement.where(json_val <= value)

        else:
            return statement.where(
                self._machinery.attributes.contains({field: value})
            )

        return statement

    def _parse_key(self, key: str) -> tuple[str, str]:
        if key.endswith("_min"):
            return key.replace("_min", ""), "ge"
        elif key.endswith("_max"):
            return key.replace("_max", ""), "le"
        return key, "eq"

    def _cast_value(self, operator: str, value: Any) -> Any:
        try:
            f_val = float(value)
            if operator in ["ge", "le"]:
                return f_val

            if f_val.is_integer():
                return int(f_val)
            return f_val
        except (ValueError, TypeError):
            if operator in ["ge", "le"]:
                return None
            return str(value)