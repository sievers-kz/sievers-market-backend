from enum import Enum


class PriceCurrency(str, Enum):
    KZT = "KZT"
    RUB = "RUB"
    USD = "USD"
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