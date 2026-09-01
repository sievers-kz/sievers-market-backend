from src.core.listing.domain.entities import Listing as DomainListing
from src.core.listing.domain.value_objects import Gallery
from src.core.listing.infrastructure.models import Listing as ORMListing


class ListingMapper:
    @staticmethod
    def to_orm(domain_model: DomainListing) -> ORMListing:
        return ORMListing(
            id=domain_model.id,
            owner_id=domain_model.owner_id,
            category_id=domain_model.category_id,
            subcategory_id=domain_model.subcategory_id,
            title=domain_model.title,
            price=domain_model.price,
            currency=domain_model.currency,
            city_id=domain_model.city_id,
            description=domain_model.description,
            attributes=domain_model.attributes,
            gallery=domain_model.gallery.to_dicts(),
            status=domain_model.status,
        )

    @staticmethod
    def to_domain(orm_model: ORMListing) -> DomainListing:
        return DomainListing(
            id=orm_model.id,
            owner_id=orm_model.owner_id,
            category_id=orm_model.category_id,
            subcategory_id=orm_model.subcategory_id,
            title=orm_model.title,
            price=orm_model.price,
            currency=orm_model.currency,
            city_id=orm_model.city_id,
            description=orm_model.description,
            attributes=orm_model.attributes,
            gallery=Gallery.from_dicts(orm_model.gallery),
            status=orm_model.status,
        )
