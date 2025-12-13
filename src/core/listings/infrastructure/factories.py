from datetime import datetime
import uuid

from src.api.listings.dto import CreateListingDTO, CreateListingMediaDTO, CreateMachineryDTO
from src.core.listings.domain.entities import Listing, ListingMedia, Machinery
from src.core.listings.domain.enums import ListingStatusEnum


class ListingFactory:
    @staticmethod
    def create(listing: CreateListingDTO, user_id: uuid.UUID) -> Listing:
        listing_id = uuid.uuid4()
        media = _ListingMediaFactory.create(listing.media, listing_id)
        machinery = _MachineryFactory.create(listing.machinery, listing_id)

        return Listing(
            id=listing_id,
            author_id=user_id,
            roubric_id=listing.roubric_id,
            region_id=listing.region_id,
            title=listing.title,
            price=listing.price,
            currency=listing.currency,
            description=listing.description,
            status=ListingStatusEnum.ACTIVE,
            media=media,
            machinery=machinery,
            updated_at=datetime.utcnow()
        )


class _ListingMediaFactory:
    @staticmethod
    def create(listing_media: list[CreateListingMediaDTO], listing_id: uuid.UUID) -> ListingMedia:
        return [
            ListingMedia(
                id=uuid.uuid4(),
                listing_id=listing_id,
                media_url=media.media_url,
                mime_type=media.mime_type,
                file_size=media.file_size,
                position=position,
                uploaded_at=datetime.utcnow()
            ) for position, media in enumerate(listing_media)
        ]


class _MachineryFactory:
    @staticmethod
    def create(machinery: CreateMachineryDTO, listing_id: uuid.UUID) -> Machinery:
        extra_specs_json = [spec.dict() for spec in machinery.extra_specs]
        return Machinery(
            id=uuid.uuid4(),
            listing_id=listing_id,
            subcategory_id=machinery.subcategory_id,
            manufacturer_id=machinery.manufacturer_id,
            manufacturer_country_id=machinery.manufacturer_country_id,
            color_id=machinery.color_id,
            model=machinery.model,
            year_of_issue=machinery.year_of_issue,
            condition=machinery.condition,
            extra_specs=extra_specs_json,
        )