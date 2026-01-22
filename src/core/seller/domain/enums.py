import enum


class SellerType(str, enum.Enum):
    IE = "ie"
    LLP = "llp"
    FARM = "farm"

    @property
    def label(self):
        labels = {
            self.IE: "Индивидуальный предприниматель",
            self.LLP: "Товарищество с ограниченной ответственностью",
            self.FARM: "Фермерское хозяйство"
        }
        return labels.get(self, "Неизвестный тип продавца")

    @property
    def tax_label(self):
        labels = {
            self.IE: "ИИН",
            self.LLP: "БИН",
            self.FARM: "ИИН/БИН"
        }
        return labels.get(self, "Неизвестный тип")