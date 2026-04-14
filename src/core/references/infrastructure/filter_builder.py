from src.core.references.presentation.dto import Option, FilterAttribute
from src.core.references.domain.enums import WidgetType
from src.core.references.infrastructure.models import SubcategoryAttribute


class FilterBuilderService:
    def build(self, items: list[SubcategoryAttribute]) -> list[FilterAttribute]:
        result = []
        for item in items:
            widget_type = self.map_widget_type(item.attribute.value_type)

            options = None
            if item.attribute.options:
                options = [
                    Option(key=option.key, label=option.label)
                    for option in item.attribute.options
                ]

            dynamic_filters = FilterAttribute(
                key=item.attribute.key,
                label=item.attribute.label,
                unit=item.unit.label if item.unit else None,
                widget_type=widget_type,
                required=item.is_required,
                options=options
            )

            result.append(dynamic_filters)
        return result

    def map_widget_type(self, value_type: str) -> str:
        mapping = {
            "integer": WidgetType.RANGE,
            "float": WidgetType.RANGE,
            "boolean": WidgetType.SWITCH,
            "enum": WidgetType.SELECT
        }
        return mapping.get(value_type, "None")