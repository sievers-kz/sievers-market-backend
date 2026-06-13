import uuid

import pytest

from src.core.vendor.domain.exceptions import InvalidLogotypeSizeError
from src.core.vendor.domain.value_objects import Logotype


class TestLogotypeValueObject:
    @pytest.mark.unit
    def test_success_logotype_creation(self):
        logotype = Logotype(
            media_id=uuid.uuid4(),
            media_type="image/jpeg",
            media_size=1 * 1024 * 1024,  # 1 MB
        )
        assert logotype is not None

    @pytest.mark.unit
    def test_logotype_exceeds_max_size_raises(self):
        with pytest.raises(InvalidLogotypeSizeError):
            Logotype(
                media_id=uuid.uuid4(),
                media_type="image/jpeg",
                media_size=Logotype.MAX_SIZE_BYTES + 1,
            )

    @pytest.mark.unit
    def test_logotype_exact_max_size_success(self):
        logotype = Logotype(
            media_id=uuid.uuid4(),
            media_type="image/jpeg",
            media_size=Logotype.MAX_SIZE_BYTES,
        )
        assert logotype.media_size == Logotype.MAX_SIZE_BYTES

    @pytest.mark.unit
    def test_logotype_from_dict_success(self):
        media_id = uuid.uuid4()
        data = {
            "media_id": str(media_id),
            "media_type": "image/jpeg",
            "media_size": 1 * 1024 * 1024,
        }
        logotype = Logotype.from_dict(data)
        assert logotype.media_id == media_id
        assert logotype.media_type == "image/jpeg"

    @pytest.mark.unit
    def test_logotype_to_dict_success(self):
        media_id = uuid.uuid4()
        logotype = Logotype(
            media_id=media_id,
            media_type="image/jpeg",
            media_size=1 * 1024 * 1024,
        )
        result = logotype.to_dict()
        assert result["media_id"] == str(media_id)
        assert result["media_type"] == "image/jpeg"
        assert result["media_size"] == 1 * 1024 * 1024
