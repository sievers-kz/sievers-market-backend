from io import BytesIO
from typing import AsyncGenerator

from minio import Minio
from rbloom import Bloom

from scripts.bloom.generate_bloom import BLOOM_OBJECT_NAME, _bloom_hash


async def init_bloom(client: Minio, bucket_name: str) -> AsyncGenerator[Bloom, None]:
    response = client.get_object(bucket_name, BLOOM_OBJECT_NAME)
    try:
        data = response.read()
    finally:
        response.close()
        response.release_conn()

    bf = Bloom.load_bytes(data, _bloom_hash)
    yield bf
