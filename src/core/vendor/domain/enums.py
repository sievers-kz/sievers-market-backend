from enum import Enum


class LegalForm(str, Enum):
    IE = "IE"  # Индивидуальный предприниматель (ИП)
    LLP = "LLP"  # Товарищество с ограниченной ответственностью (ТОО)
    JSC = "JSC"  # Акционерное общество (АО)
    FARM = "FARM"  # Крестьянское / Фермерское хозяйтсво


class VendorStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    BANNED = "banned"
