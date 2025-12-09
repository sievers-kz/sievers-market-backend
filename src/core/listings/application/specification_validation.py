from src.core.references.domain.enums import MachinerySpecsValueTypeEnum


TYDED_CASTS = {
    MachinerySpecsValueTypeEnum.INTEGER.value: lambda v: int(v),
    MachinerySpecsValueTypeEnum.FLOAT.value: lambda v: float(v),
    MachinerySpecsValueTypeEnum.STRING.value: lambda v: str(v),
    MachinerySpecsValueTypeEnum.BOOLEAN.value: lambda v: bool(v),
    MachinerySpecsValueTypeEnum.ENUM.value: lambda v: v
}


def validate_specification_fields(extra_specifications, allowed_specifications) -> None:
    """
    Проверяет типы, юниты и обязательные поля в списке extra_specifications.
    Приводит типы (int, float) на месте. При ошибке - бросает ValueError.
    """

    allowed_by_key = {}
    for ref in allowed_specifications:
        allowed_by_key.setdefault(ref.key, []).append(ref)

    for spec in extra_specifications:
        if spec.key not in allowed_by_key:
            raise ValueError("Недопустимая спецификация")

        refs = allowed_by_key[spec.key]

        allowed_options = [item for r in refs if r.options for item in r.options]
        if allowed_options and spec.value not in allowed_options:
            raise ValueError(f"Недопустимые опции для {spec.key}")

        allowed_units = [r.unit for r in refs if r.unit is not None]
        if allowed_units and spec.unit not in allowed_units:
            raise ValueError("Недопустимая единица измерения")

        system_type = refs[0].value_type

        caster = TYDED_CASTS.get(system_type)
        if caster is None:
            raise ValueError(f"Такой тип данных ({caster}) не поддерживается")

        try:
            spec.value = caster(spec.value)
        except Exception:
            raise ValueError(f"Вы ввели некорректный тип данных для: {spec.key}")

    return
