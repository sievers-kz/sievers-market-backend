from typing import Protocol


class OrganizationProfile(Protocol):
    """Anything that carries the organization profile fields: the aggregate or a database row."""

    shop_name: str | None
    contact_phone: str | None
    contact_email: str | None


def missing_profile_fields(organization: OrganizationProfile) -> list[str]:
    """Profile fields the owner must fill before the organization may publish listings.

    The only place that says which fields are required. The aggregate uses it to reject publishing,
    and the query service uses it to tell the UI what is left to fill, without loading the aggregate.
    """
    required = {
        "shop_name": organization.shop_name,
        "contact_phone": organization.contact_phone,
        "contact_email": organization.contact_email,
    }
    return [name for name, value in required.items() if not value]
