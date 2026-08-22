import hashlib
from pathlib import Path

from loguru import logger
from rbloom import Bloom

BASE_DIR = Path(__file__).parent
WORDLIST_DIR = BASE_DIR / "wordlist"

TXT_PATH = WORDLIST_DIR / "weak_passwords.txt"
BLOOM_PATH = WORDLIST_DIR / "weak_passwords.bloom"

CAPACITY = 1_100_000
ERROR_RATE = 0.01


def _bloom_hash(item: str) -> int:
    return int(hashlib.sha256(item.encode("utf-8")).hexdigest(), 16) % (2**61 - 1)


def generate_bloom() -> None:
    if not TXT_PATH.exists():
        logger.warning(f"Файл {TXT_PATH.name} не найден. Генерация пропущена.")
        return

    logger.info(f"Запуск генерации Bloom-фильтра из {TXT_PATH.name}")
    bf = Bloom(CAPACITY, ERROR_RATE, _bloom_hash)
    count = 0

    with open(TXT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            password = raw_line.strip()
            if password:
                bf.add(password)
                count += 1

    bloom_bytes = bf.save_bytes()
    WORDLIST_DIR.mkdir(parents=True, exist_ok=True)

    with open(BLOOM_PATH, "wb") as f:
        f.write(bloom_bytes)
    logger.info(f"Bloom файл успешно сохранен в {BLOOM_PATH.name}")

    TXT_PATH.unlink()
    logger.info(f"Файл {TXT_PATH.name} безвозвратно удален.")


if __name__ == "__main__":
    generate_bloom()
