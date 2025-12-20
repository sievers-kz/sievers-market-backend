from sqlalchemy import event
from src.core.listings.infrastructure.models.listing import Listing  # Импортируй свою модель


@event.listens_for(Listing, 'before_insert')
@event.listens_for(Listing, 'before_update')
def update_listing_search_index(mapper, connection, target: Listing):
    parts = [
        target.title,
        target.description,
        target.region.name if target.region else "",
        target.machinery.manufacturer.manufacturer_name if target.machinery and target.machinery.manufacturer else "",
        target.machinery.model if target.machinery else ""
    ]

    if target.machinery and target.machinery.extra_specs:
        for spec in target.machinery.extra_specs:
            val = f"{spec.get('key', '')} {spec.get('value', '')} {spec.get('unit', '')}"
            parts.append(val)

    target.search_content = " ".join(filter(None, parts)).lower()