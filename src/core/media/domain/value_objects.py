from dataclasses import dataclass


@dataclass(frozen=True)
class MediaSize:
    MAX_SIZE_BYTES = 20 * 1024 * 1024
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Размер файла должен быть больше нуля")
        if self.value > self.MAX_SIZE_BYTES:
            raise ValueError("Изображение слишком велико. Допустимо до 20 МБ")
