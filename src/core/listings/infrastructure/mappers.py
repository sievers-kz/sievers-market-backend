from src.core.listings.domain.entities import (
    Listing as DomainListing,
    ListingMedia as DomainListingMedia,
    Machinery as DomainMachinery
)

from src.core.listings.infrastructure.models.listing import Listing as ORMListing, ListingMedia as ORMListingMedia
from src.core.listings.infrastructure.models.machinery import Machinery as ORMMachinery


class ListingMapper:
    @staticmethod
    def to_domain(orm_model: ORMListing) -> DomainListing:
        media = [ListingMediaMapper.to_domain(media) for media in orm_model.media]
        machinery = MachineryMapper.to_domain(orm_model.machinery)

        return DomainListing(
            id=orm_model.id,
            author_id=orm_model.author_id,
            roubric_id=orm_model.roubric_id,
            region_id=orm_model.region_id,
            title=orm_model.title,
            price=orm_model.price,
            currency=orm_model.currency,
            description=orm_model.description,
            status=orm_model.status,
            media=media,
            machinery=machinery
        )

    @staticmethod
    def to_orm(domain_model: DomainListing) -> ORMListing:
        media = [ListingMediaMapper.to_orm(media) for media in domain_model.media]
        machinery = MachineryMapper.to_orm(domain_model.machinery)

        return ORMListing(
            id=domain_model.id,
            author_id=domain_model.author_id,
            roubric_id=domain_model.roubric_id,
            region_id=domain_model.region_id,
            title=domain_model.title,
            price=domain_model.price,
            currency=domain_model.currency,
            description=domain_model.description,
            status=domain_model.status,
            media=media,
            machinery=machinery
        )


class ListingMediaMapper:
    @staticmethod
    def to_domain(orm_model: ORMListingMedia) -> DomainListingMedia:
        return DomainListingMedia(
            id=orm_model.id,
            listing_id=orm_model.listing_id,
            media_url=orm_model.media_url,
            mime_type=orm_model.mime_type,
            is_main=orm_model.is_main,
            file_size=orm_model.file_size,
            position=orm_model.position,
            uploaded_at=orm_model.uploaded_at
        )

    @staticmethod
    def to_orm(domain_model: DomainListingMedia) -> ORMListingMedia:
        return ORMListingMedia(
            id=domain_model.id,
            listing_id=domain_model.listing_id,
            media_url=domain_model.media_url,
            mime_type=domain_model.mime_type,
            is_main=domain_model.is_main,
            file_size=domain_model.file_size,
            position=domain_model.position,
            uploaded_at=domain_model.uploaded_at
        )


class MachineryMapper:
    @staticmethod
    def to_domain(orm_model: ORMMachinery) -> DomainMachinery:
        return DomainMachinery(
            id=orm_model.id,
            listing_id=orm_model.listing_id,
            subcategory_id=orm_model.subcategory_id,
            manufacturer_id=orm_model.manufacturer_id,
            manufacturer_country_id=orm_model.manufacturer_country_id,
            color_id=orm_model.color_id,
            model=orm_model.model,
            year_of_issue=orm_model.year_of_issue,
            condition=orm_model.condition,
            extra_specs=orm_model.extra_specs
        )

    @staticmethod
    def to_orm(domain_model: DomainMachinery) -> ORMMachinery:
        return ORMMachinery(
            id=domain_model.id,
            listing_id=domain_model.listing_id,
            subcategory_id=domain_model.subcategory_id,
            manufacturer_id=domain_model.manufacturer_id,
            manufacturer_country_id=domain_model.manufacturer_country_id,
            color_id=domain_model.color_id,
            model=domain_model.model,
            year_of_issue=domain_model.year_of_issue,
            condition=domain_model.condition,
            extra_specs=domain_model.extra_specs
        )