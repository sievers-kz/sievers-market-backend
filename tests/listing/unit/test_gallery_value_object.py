import uuid

import pytest

from src.core.listing.domain.exceptions import (
    ListingGalleryEmptyError,
    ListingGalleryTooManyImagesError,
    ListingLargeImageSizeError,
)
from src.core.listing.domain.value_objects import Gallery, Image


def create_image(media_size=1 * 1024 * 1024) -> Image:
    return Image(
        media_id=uuid.uuid4(),
        media_type="image/jpeg",
        media_size=media_size,
    )


class TestImageValueObject:

    @pytest.mark.unit
    def test_create_image_success(self):
        image = create_image()
        assert image is not None

    @pytest.mark.unit
    def test_image_exact_max_size_success(self):
        image = create_image(media_size=Image.MAX_SIZE_BYTES)
        assert image.media_size == Image.MAX_SIZE_BYTES

    @pytest.mark.unit
    def test_image_exceeds_max_size_raises(self):
        with pytest.raises(ListingLargeImageSizeError):
            create_image(media_size=Image.MAX_SIZE_BYTES + 1)

    @pytest.mark.unit
    def test_image_from_dict_success(self):
        media_id = uuid.uuid4()
        data = {
            "media_id": str(media_id),
            "media_type": "image/jpeg",
            "media_size": 1 * 1024 * 1024,
        }
        image = Image.from_dict(data)
        assert image.media_id == media_id
        assert image.media_type == "image/jpeg"

    @pytest.mark.unit
    def test_image_to_dict_success(self):
        media_id = uuid.uuid4()
        image = Image(
            media_id=media_id,
            media_type="image/jpeg",
            media_size=1 * 1024 * 1024,
        )
        result = image.to_dict()
        assert result["media_id"] == str(media_id)
        assert result["media_type"] == "image/jpeg"
        assert result["media_size"] == 1 * 1024 * 1024


class TestGalleryValueObject:

    @pytest.mark.unit
    def test_create_gallery_success(self):
        gallery = Gallery(images=tuple(create_image() for _ in range(3)))
        assert len(gallery.images) == 3

    @pytest.mark.unit
    def test_gallery_empty_raises(self):
        with pytest.raises(ListingGalleryEmptyError):
            Gallery(images=())

    @pytest.mark.unit
    def test_gallery_max_images_success(self):
        gallery = Gallery(images=tuple(create_image() for _ in range(10)))
        assert len(gallery.images) == 10

    @pytest.mark.unit
    def test_gallery_too_many_images_raises(self):
        with pytest.raises(ListingGalleryTooManyImagesError):
            Gallery(images=tuple(create_image() for _ in range(11)))

    @pytest.mark.unit
    def test_gallery_from_dicts_success(self):
        data = [
            {
                "media_id": str(uuid.uuid4()),
                "media_type": "image/jpeg",
                "media_size": 1 * 1024 * 1024,
            }
            for _ in range(3)
        ]
        gallery = Gallery.from_dicts(data)
        assert len(gallery.images) == 3

    @pytest.mark.unit
    def test_gallery_to_dicts_success(self):
        gallery = Gallery(images=tuple(create_image() for _ in range(3)))
        result = gallery.to_dicts()
        assert len(result) == 3
        assert "media_id" in result[0]
        assert "media_type" in result[0]
        assert "media_size" in result[0]
