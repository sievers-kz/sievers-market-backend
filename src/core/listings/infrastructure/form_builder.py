from typing import List

from src.api.listings.dto import FieldFormGroupDTO, FieldFormDTO, FieldTypeEnum, FieldOptionDTO
from src.api.references.dto import RegionDTO, ManufacturerDTO, ManufactureCountryDTO, ColorDTO, SpecificationDTO
from src.core.listings.domain.enums import MachineryConditionEnum, ListingCurrencyEnum


class ListingFormBuilderService:
    def build_form_schema(
        self,
        specifications: List[SpecificationDTO]
    ):
        schema = [
            self._build_basic_schema(),
            self._build_machinery_group(),
            self._build_specifications_group(specifications)
        ]

        return schema

    def _build_basic_schema(self):
        return FieldFormGroupDTO(
            id="basic_info",
            title="Основная информация",
            order=1,
            fields=[
                FieldFormDTO(
                    name="title",
                    label="Заголовок",
                    type=FieldTypeEnum.TEXT,
                    required=True,
                    placeholder="Например: Трактор John Deere 8R"
                ),
                FieldFormDTO(
                    name="region_id",
                    label="Регион",
                    type=FieldTypeEnum.SELECT,
                    required=True,
                ),
                FieldFormDTO(
                    name="price",
                    label="Цена",
                    type=FieldTypeEnum.NUMBER,
                    required=True
                ),
                FieldFormDTO(
                    name="currency",
                    label="Валюта",
                    type=FieldTypeEnum.SELECT,
                    required=True,
                    options=[
                        FieldOptionDTO(value=option, label=option)
                        for option in ListingCurrencyEnum
                    ]
                ),
                FieldFormDTO(
                    name="description",
                    label="Описание",
                    type=FieldTypeEnum.TEXTAREA,
                    required=False,
                    placeholder="Подробно опишите технику"
                ),
            ]
        )

    def _build_machinery_group(self) -> FieldFormGroupDTO:
        """Характеристики техники (Machinery)"""
        return FieldFormGroupDTO(
            id="machinery",
            title="Характеристики техники",
            order=2,
            fields=[
                FieldFormDTO(
                    name="manufacturer_id",
                    label="Производитель",
                    type=FieldTypeEnum.SELECT,
                    required=True,
                ),
                FieldFormDTO(
                    name="model",
                    label="Модель",
                    type=FieldTypeEnum.TEXT,
                    required=True,
                    placeholder="Например: 8R 370"
                ),
                FieldFormDTO(
                    name="year_of_issue",
                    label="Год выпуска",
                    type=FieldTypeEnum.NUMBER,
                    required=True,
                ),
                FieldFormDTO(
                    name="condition",
                    label="Состояние",
                    type=FieldTypeEnum.SELECT,
                    required=True,
                    options=[
                        FieldOptionDTO(value=opt, label=opt)
                        for opt in MachineryConditionEnum
                    ]
                ),
                FieldFormDTO(
                    name="color_id",
                    label="Цвет",
                    type=FieldTypeEnum.SELECT,
                    required=False,
                ),
            ]
        )

    def _build_specifications_group(
        self,
        specifications: List[SpecificationDTO]
    ) -> FieldFormGroupDTO:
        """Дополнительные характеристики (динамические)"""
        fields = []

        for spec in specifications:
            field = FieldFormDTO(
                name=spec.key,
                label=spec.label,
                type=self._map_value_type(spec.value_type),
                required=spec.is_required,
                options=[
                    FieldOptionDTO(
                        value=option, label=option
                    )for option in spec.options
                ] if spec.options else None,
                extra={"unit": spec.unit}
            )

            fields.append(field)
        return FieldFormGroupDTO(
            id="specifications",
            title="Дополнительные характеристики",
            order=3,
            fields=fields
        )

    @staticmethod
    def _map_value_type(value_type: str) -> FieldTypeEnum:
        """Маппинг типов"""
        mapping = {
            "integer": FieldTypeEnum.NUMBER,
            "float": FieldTypeEnum.NUMBER,
            "string": FieldTypeEnum.TEXT,
            "enum": FieldTypeEnum.SELECT,
        }
        return mapping.get(value_type, FieldTypeEnum.TEXT)