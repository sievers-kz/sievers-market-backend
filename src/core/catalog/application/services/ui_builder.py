from src.core.references.domain.enums import WidgetType
from src.core.references.infrastructure.models import SubcategoryAttribute
from src.core.references.presentation.dto.subcategory_attribute import UIField, MachineryFormConfig, \
    MachineryFilterConfig, LivestockFormConfig, LivestockFilterConfig


class UIBuilderService:
    def __init__(self):
        self.form_config = {
            "Техника": MachineryFormConfig(),
            "Животноводство": LivestockFormConfig()
        }

        self.filter_config = {
            "Техника": MachineryFilterConfig(),
            "Животноводство": LivestockFilterConfig()
        }

    def to_form(self, rubric: str, attributes: list[SubcategoryAttribute]) -> list[UIField]:
        result: list[UIField] = []

        config = self.form_config.get(rubric)
        if config:
            for field in config.fields:
                result.append(UIField(**field))

        for item in attributes:

            result.append(
                UIField(
                    key=item.attribute.key,
                    label=item.attribute.label,
                    unit=item.unit.name if item.unit else None,
                    widget_type=self._get_form_widget(item.attribute.value_type),
                    required=item.is_required,
                    options=item.attribute.options or [],
                )
            )

        return result

    def to_filter(self, rubric: str, attributes: list[SubcategoryAttribute]) -> list[UIField]:
        result: list[UIField] = []

        config = self.filter_config.get(rubric)
        if config:
            for field in config.fields:
                result.append(UIField(**field))

        for item in attributes:
            if not item.is_filterable:
                continue

            result.append(
                UIField(
                    key=item.attribute.key,
                    label=item.attribute.label,
                    unit=item.unit.name if item.unit else None,
                    widget_type=self._get_filter_widget(item.attribute.value_type),
                    options=item.attribute.options or [],
                )
            )

        return result

    def _get_form_widget(self, value_type: str) -> str:
        mapping = {
            "integer": WidgetType.NUMBER,
            "float": WidgetType.NUMBER,
            "string": WidgetType.TEXT,
            "enum": WidgetType.SELECT,
            "boolean": WidgetType.SWITCH,
        }
        return mapping.get(value_type, WidgetType.TEXT)

    def _get_filter_widget(self, value_type: str) -> str:
        if value_type in ("integer", "float"):
            return WidgetType.RANGE

        mapping = {
            "string": WidgetType.TEXT,
            "enum": WidgetType.SELECT,
            "boolean": WidgetType.SWITCH,
        }
        return mapping.get(value_type, WidgetType.TEXT)
