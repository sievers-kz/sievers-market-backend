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