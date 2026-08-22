from pathlib import Path

from loguru import logger
from rbloom import Bloom

from scripts.bloom.generate_bloom import _bloom_hash

BASE_DIR = Path(__file__).parent
BLOOM_PATH = BASE_DIR / "wordlist" / "weak_passwords.bloom"


def load_bloom() -> Bloom:
    if not BLOOM_PATH.exists():
        logger.info(f"Не удалось найти бинарный файл {BLOOM_PATH.name}")
        return

    with open(BLOOM_PATH, "rb") as f:
        data = f.read()

    bf = Bloom.load_bytes(data, _bloom_hash)
    logger.info("Bloom успешно загружен")

    return bf
