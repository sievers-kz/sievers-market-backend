from src.api.listings.dto import FilterBlocks, FilterFields, BaseFilters, FilterTypes, DynamicFilters, SidebarFilters, \
    FilterOptions, FilterRanges
from src.core.references.domain.enums import MachinerySpecsValueTypeEnum


class FilterBuilderService:
    def build_filters(self, base_filters: BaseFilters, dynamic_filters: DynamicFilters):
        base = self.build_base_filters(base_filters)
        dynamic = self.build_dynamic_filters(dynamic_filters)
        return SidebarFilters(base_filters=base, dynamic_filters=dynamic)

    def build_base_filters(self, base_filters: BaseFilters):
        blocks = []

        categories_fields = FilterFields(
            name="subcategory_id",
            label="Подкатегории",
            type=FilterTypes.SELECT,
            unit=None,
            placeholder=None,
            options=[
                FilterOptions(
                    value=sub["id"], label=sub["name"]
                ) for sub in base_filters.subcategories
            ]
        )

        blocks.append(
            FilterBlocks(
                id="categories_block",
                title="Категории",
                order=0,
                filters=[categories_fields]
            )
        )

        price_field = FilterFields(
            name="price",
            label="Цена",
            type=FilterTypes.RANGE,
            unit=None,
            options=[],
            ranges=FilterRanges(
                min_label="От",
                max_label="До"
            )
        )

        blocks.append(
            FilterBlocks(
                id="price_block",
                title="Цена",
                filters=[price_field],
                order=1
            )
        )

        return blocks

    def build_dynamic_filters(self, dynamic_filters: list[DynamicFilters]):
        if not dynamic_filters:
            return []

        dynamic_filter_blocks = []
        current_order = 2
        for spec in dynamic_filters:
            ranges = None

            if spec.type in [MachinerySpecsValueTypeEnum.INTEGER.value, MachinerySpecsValueTypeEnum.FLOAT.value]:
                ranges = FilterRanges(min_label="От", max_label="До")

            dynamic_filter_blocks.append(
                FilterBlocks(
                    id=f"filter_{spec.key}_block",
                    title=spec.label,
                    order=current_order,
                    filters=[
                        FilterFields(
                            name=spec.key,
                            label=spec.label,
                            type=self._map_value_type(spec.type),
                            unit=spec.unit if spec.unit else None,
                            ranges=ranges,
                            options=spec.options if spec.options else []
                        )
                    ]
                )
            )
            current_order += 1

        return dynamic_filter_blocks

    @staticmethod
    def _map_value_type(value_type: str) -> FilterTypes:
        """Маппинг типов"""
        mapping = {
            "integer": FilterTypes.RANGE,
            "float": FilterTypes.RANGE,
            "string": FilterTypes.SELECT,
            "enum": FilterTypes.SELECT,
        }
        return mapping.get(value_type, FilterTypes.SELECT)