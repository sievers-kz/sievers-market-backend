from src.api.reference.dto import MachineryConfig, LivestockConfig, FormField, Option
from src.core.references.domain.enums import WidgetType
from src.core.references.infrastructure.models import SubcategoryAttribute


class FormBuilderService:
    def __init__(self):
        self.configs = {
            "Техника": MachineryConfig(),
            "Животноводство": LivestockConfig()
        }

    def build(self, rubric: str, attributes: list[SubcategoryAttribute]):
        result = []

        config = self.configs.get(rubric)
        if config:
            for field in config.fields:
                result.append(FormField(**field))

        for item in attributes:
            widget_type = self._map_widget_type(item.attribute.value_type)

            options = None
            if item.attribute.options:
                options = [
                    Option(key=option.key, label=option.label)
                    for option in item.attribute.options
                ]

            dynamic_field = FormField(
                key=item.attribute.key,
                label=item.attribute.label,
                unit=item.unit.label if item.unit else None,
                widget_type=widget_type,
                required=item.is_required,
                options=options
            )

            result.append(dynamic_field)
        return result

    def _map_widget_type(self, value_type: str) -> str:
        mapping = {
            "integer": WidgetType.NUMBER,
            "float": WidgetType.NUMBER,
            "string": WidgetType.TEXT,
            "enum": WidgetType.SELECT,
            "boolean": WidgetType.SWITCH
        }
        return mapping.get(value_type, "text")