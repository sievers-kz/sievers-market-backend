"""Маски контактов продавца для детальной карточки.

Полные телефон и email отдаёт только `GET /listing/{id}/contacts`: в ответе детальной (и в HTML страницы)
лежит маска, чтобы номер нельзя было собрать простым парсингом страниц.
"""

import re

MASK = "•"


def mask_phone(phone: str | None) -> str | None:
    """`+77472006243` -> `+7 747 2•• •• ••`.

    Казахстанский номер (11 цифр с 7 или 8 в начале) форматируется; у остальных видны первые 4 цифры.
    """
    if not phone or not phone.strip():
        return None

    digits = re.sub(r"\D", "", phone)
    if not digits:
        return None

    if len(digits) == 11 and digits[0] in "78":
        local = digits[1:]
        return f"+7 {local[:3]} {local[3]}{MASK * 2} {MASK * 2} {MASK * 2}"

    visible = digits[:4]
    return f"+{visible}{MASK * max(len(digits) - 4, 3)}"


def mask_email(email: str | None) -> str | None:
    """`sales@olzha-agro.kz` -> `s••••@olzha-agro.kz`. Домен виден: по нему понятно, что это почта компании."""
    if not email or not email.strip():
        return None

    local, separator, domain = email.strip().partition("@")
    if not separator or not local or not domain:
        return MASK * 4

    return f"{local[0]}{MASK * 4}@{domain}"
