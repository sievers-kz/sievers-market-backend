from enum import Enum


class ListingStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"

    @property
    def label(self):
        labels = {
            self.ACTIVE: "Активный",
            self.INACTIVE: "Неактивный",
            self.ARCHIVED: "Архив",
            self.DELETED: "Удален"
        }
        return labels.get(self, "Неизвестное состояние")