from enum import Enum


class MachineryCondition(str, Enum):
    NEW = "new"
    USED = "used"

    @property
    def label(self):
        labels = {
            self.NEW: "Новый",
            self.USED: "Б/У"
        }
        return labels.get(self, "Неизвестное состояние")


class PriceCurrency(str, Enum):
    KZT = "KZT"
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class ListingStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DRAFT = "draft"
    DELETED = "deleted"

    @property
    def label(self):
        labels = {
            self.ACTIVE: "Активный",
            self.INACTIVE: "Неактивный",
            self.DRAFT: "Черновик",
            self.ARCHIVED: "Архив",
            self.DELETED: "Удален"
        }
        return labels.get(self, "Неизвестное состояние")