from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.core.catalog.infrastructure.catalog_service import CatalogService
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError


def make_service(category_exists: bool, subcategory_category_id=None) -> CatalogService:
    category_repo = AsyncMock()
    category_repo.get_by_id.return_value = object() if category_exists else None
    subcategory_repo = AsyncMock()
    subcategory_repo.get_by_id.return_value = (
        SimpleNamespace(category_id=subcategory_category_id) if subcategory_category_id else None
    )
    return CatalogService(category_repo=category_repo, subcategory_repo=subcategory_repo)


@pytest.mark.asyncio
async def test_subcategory_in_category_passes():
    category_id = uuid4()
    service = make_service(category_exists=True, subcategory_category_id=category_id)

    await service.ensure_subcategory_in_category(category_id, uuid4())


@pytest.mark.asyncio
async def test_unknown_category_raises_with_category_field():
    category_id = uuid4()
    service = make_service(category_exists=False, subcategory_category_id=category_id)

    with pytest.raises(CatalogNotFoundError) as exc:
        await service.ensure_subcategory_in_category(category_id, uuid4())

    assert exc.value.metadata == {"field": str(category_id)}


@pytest.mark.asyncio
async def test_unknown_subcategory_raises_with_subcategory_field():
    subcategory_id = uuid4()
    service = make_service(category_exists=True, subcategory_category_id=None)

    with pytest.raises(CatalogNotFoundError) as exc:
        await service.ensure_subcategory_in_category(uuid4(), subcategory_id)

    assert exc.value.metadata == {"field": str(subcategory_id)}


@pytest.mark.asyncio
async def test_subcategory_from_another_category_raises():
    subcategory_id = uuid4()
    service = make_service(category_exists=True, subcategory_category_id=uuid4())

    with pytest.raises(CatalogNotFoundError) as exc:
        await service.ensure_subcategory_in_category(uuid4(), subcategory_id)

    assert exc.value.metadata == {"field": str(subcategory_id)}
