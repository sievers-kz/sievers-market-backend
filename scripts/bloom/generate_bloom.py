"""
scripts/bloom/generate_bloom.py

Генерирует bloom-фильтр из списка 1 000 000 утекших паролей
и загружает бинарный файл в MinIO.

Запуск: python -m scripts.bloom.generate_bloom
"""

import hashlib
import sys
import urllib.request
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
from rbloom import Bloom

from src.configuration.settings.settings import MinioConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    print(f"✅ .env loaded from {ENV_PATH}")
else:
    print(f"⚠️  .env not found at {ENV_PATH}, relying on environment variables")


PASSWORDS_URL = (
    "https://raw.githubusercontent.com/danielmiessler/SecLists"
    "/master/Passwords/Common-Credentials/xato-net-10-million-passwords-1000000.txt"
)

BLOOM_OBJECT_NAME = "bloom/weak_passwords.bloom"
CAPACITY = 1_100_000
ERROR_RATE = 0.01


def _bloom_hash(item: str) -> int:
    return int(hashlib.sha256(item.encode("utf-8")).hexdigest(), 16) % (2**61 - 1)


class BloomGenerator:
    def __init__(self, config: MinioConfig):
        self._client = Minio(
            endpoint=config.endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=config.secure_config,
        )
        self._bucket = config.bucket_name

    def run(self) -> None:
        if self._exists():
            return
        bf = self._build_from_url()
        self._upload(bf)
        print("🚀 Done!")

    def _exists(self) -> bool:
        """
        HEAD-запрос к MinIO — не читает содержимое, только метаданные.
        Ловим только NoSuchKey: любая другая S3Error (нет доступа,
        нет бакета) пробрасывается наружу — скрипт падает с ненулевым
        кодом и init-контейнер не даёт стартовать app.
        """
        try:
            self._client.stat_object(self._bucket, BLOOM_OBJECT_NAME)
            print(
                f"✅ Bloom filter already exists at "
                f"{self._bucket}/{BLOOM_OBJECT_NAME} — nothing to do"
            )
            return True
        except S3Error as e:
            if e.code in ("NoSuchKey", "NoSuchBucket"):
                return False
            raise

    def _build_from_url(self) -> Bloom:
        """
        Скачивает список паролей и сразу строит фильтр построчно —
        без промежуточного хранения всего списка в памяти.

        Явный User-Agent обязателен — GitHub блокирует дефолтный Python-агент.
        Тайм-аут 60 сек защищать от зависания в CI.
        """
        print("⬇️  Downloading and building bloom filter...")
        print(f"    {PASSWORDS_URL}")

        req = urllib.request.Request(
            PASSWORDS_URL,
            headers={"User-Agent": "agrow-bloom-generator/1.0"},
        )

        bf = Bloom(CAPACITY, ERROR_RATE, _bloom_hash)
        count = 0

        with urllib.request.urlopen(req, timeout=60) as response:
            for raw_line in response:
                password = raw_line.decode("utf-8", errors="ignore").strip()
                if password:
                    bf.add(password)
                    count += 1

        print(f"✅ Built — {count:,} entries")
        return bf

    def _upload(self, bf: Bloom) -> None:
        data = bf.save_bytes()  # bytes
        size = len(data)
        size_kb = size / 1024

        print(
            f"⬆️  Uploading to {self._bucket}/{BLOOM_OBJECT_NAME} "
            f"({size_kb:.1f} KB)..."
        )

        if not self._client.bucket_exists(self._bucket):
            self._client.make_bucket(self._bucket)
            print(f"🪣 Bucket '{self._bucket}' created")

        self._client.put_object(
            bucket_name=self._bucket,
            object_name=BLOOM_OBJECT_NAME,
            data=BytesIO(data),
            length=size,
            content_type="application/octet-stream",
        )
        print(f"✅ Uploaded ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    BloomGenerator(MinioConfig()).run()
    sys.exit(0)
