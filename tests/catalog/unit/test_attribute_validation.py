from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.core.catalog.infrastructure.attribute_validation import (
    AttributeValidationService,
)
from src.core.catalog.infrastructure.enums import AttributeType
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError


def make_service(subcategory_exists: bool, links: list) -> AttributeValidationService:
    link_repo = AsyncMock()
    link_repo.get_with_definitions.return_value = links
    subcategory_repo = AsyncMock()
    subcategory_repo.get_by_id.return_value = object() if subcategory_exists else None
    return AttributeValidationService(
        link_repo=link_repo, subcategory_repo=subcategory_repo
    )


def make_link(key: str, attr_type: AttributeType, required: bool):
    return SimpleNamespace(
        attribute=SimpleNamespace(key=key, type=attr_type), required=required
    )


@pytest.mark.asyncio
async def test_subcategory_without_attributes_is_valid():
    service = make_service(subcategory_exists=True, links=[])

    assert await service.validate(uuid4(), {}) == {}


@pytest.mark.asyncio
async def test_unknown_subcategory_raises_not_found():
    service = make_service(subcategory_exists=False, links=[])

    with pytest.raises(CatalogNotFoundError):
        await service.validate(uuid4(), {})


@pytest.mark.asyncio
async def test_validates_attributes_when_configured():
    links = [make_link("engine_power", AttributeType.INTEGER, required=True)]
    service = make_service(subcategory_exists=True, links=links)

    assert await service.validate(uuid4(), {"engine_power": 123}) == {
        "engine_power": 123
    }
