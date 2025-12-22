from datetime import datetime
import uuid

from src.api.listings.dto import (
    CreateActiveListingDTO,
    CreateListingMediaDTO,
    CreateMachineryDTO,
    CreateDraftListingDTO,
    CreateDraftListingMediaDTO,
    CreateDraftMachineryDTO
)
from src.core.listings.domain.entities import Listing, ListingMedia, Machinery
from src.core.listings.domain.value_objects import Title, Price, Model, YearOfIssue


class ListingFactory:
    @staticmethod
    def create(listing: CreateActiveListingDTO | CreateDraftListingDTO, user_id: uuid.UUID) -> Listing:
        listing_id = uuid.uuid4()
        media = (_ListingMediaFactory.create(listing.media, listing_id) if listing.media else [])
        machinery = (_MachineryFactory.create(listing.machinery, listing_id) if listing.machinery else None)

        return Listing(
            id=listing_id,
            author_id=user_id,
            roubric_id=listing.roubric_id,
            region_id=listing.region_id,
            title=Title.from_raw(listing.title),
            price=Price.from_raw(listing.price),
            currency=listing.currency,
            description=listing.description,
            status=None,
            media=media,
            machinery=machinery,
            updated_at=datetime.utcnow()
        )


class _ListingMediaFactory:
    @staticmethod
    def create(
        listing_media: list[CreateListingMediaDTO | CreateDraftListingMediaDTO],
        listing_id: uuid.UUID
    ) -> ListingMedia:
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
    def create(machinery: CreateMachineryDTO | CreateDraftMachineryDTO, listing_id: uuid.UUID) -> Machinery:
        extra_specs_json = [spec.dict() for spec in machinery.extra_specs] if machinery.extra_specs else []
        return Machinery(
            id=uuid.uuid4(),
            listing_id=listing_id,
            subcategory_id=machinery.subcategory_id,
            manufacturer_id=machinery.manufacturer_id,
            manufacturer_country_id=machinery.manufacturer_country_id,
            color_id=machinery.color_id,
            model=Model.from_raw(machinery.model),
            year_of_issue=YearOfIssue.from_raw(machinery.year_of_issue),
            condition=machinery.condition,
            extra_specs=extra_specs_json,
        )