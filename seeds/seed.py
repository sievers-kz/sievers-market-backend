import yaml
import logging
from pathlib import Path
from typing import Any, List, Dict

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from seeds.schemas import RubricSeed, ColorSeed, BrandSeed
from src.configuration.settings.settings import PostgresSettings
from src.core.catalog.domain.enums import CatalogStatus

from src.core.catalog.infrastructure.models import Rubric, Category, Subcategory
from src.core.references.infrastructure.models import Brand, Country, Color, Region, City

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    print(f"✅ .env loaded from {ENV_PATH}")
else:
    print(f"❌ .env NOT FOUND at {ENV_PATH}")

from src.configuration.settings.settings import PostgresSettings


logger = logging.getLogger(__name__)


class DataSeeder:
    def __init__(self, session: AsyncSession):
        self.session = session
        # Путь к папке с фикстурами
        self.data_dir = Path(__file__).resolve().parent / "data"
        print(self.data_dir)

    def _load_yaml(self, file_name: str) -> Any:
        """Универсальный метод для загрузки YAML файлов"""
        file_path = self.data_dir / file_name
        print(f"FILE PATH: {file_path}")
        if not file_path.exists():
            logger.error(f"❌ File not found: {file_path}")
            return None

        logger.info(f"📂 Loading YAML: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    async def seed_brands(self):
        raw_data = self._load_yaml("brands.yaml")
        if not raw_data:
            return

        try:
            adapter = TypeAdapter(list[BrandSeed])
            brands = adapter.validate_python(raw_data)

            for brand_dto in brands:
                self.session.add(Brand(name=brand_dto.name))
            logger.info("✅ Brands seeded with DTO")
        except Exception as e:
            logger.error(f"❌ Brand validation failed: {e}")
            raise

    async def seed_colors(self):
        raw_data = self._load_yaml("colors.yaml")
        if not raw_data:
            return

        adapter = TypeAdapter(list[ColorSeed])
        colors = adapter.validate_python(raw_data)

        for color_dto in colors:
            self.session.add(Color(name=color_dto.name, hex=color_dto.hex))
        logger.info("✅ Colors seeded with DTO")

    async def seed_catalog_hierarchy(self):
        raw_data = self._load_yaml("categories.yaml")
        if not raw_data:
            return

        adapter = TypeAdapter(list[RubricSeed])
        rubrics_data = adapter.validate_python(raw_data)

        for r_dto in rubrics_data:
            rubric = Rubric(
                name=r_dto.name,
                attributes=[a.model_dump() for a in r_dto.attributes],
                status=CatalogStatus.ACTIVE
            )
            self.session.add(rubric)
            await self.session.flush()

            for c_dto in r_dto.categories:
                category = Category(
                    rubric_id=rubric.id,
                    name=c_dto.name,
                    status=CatalogStatus.ACTIVE
                )
                self.session.add(category)
                await self.session.flush()

                for s_dto in c_dto.subcategories:
                    subcategory = Subcategory(
                        category_id=category.id,
                        name=s_dto.name,
                        attributes=[a.model_dump() for a in s_dto.attributes],
                        status=CatalogStatus.ACTIVE
                    )
                    self.session.add(subcategory)

        logger.info("✅ Catalog hierarchy seeded with Pydantic validation")

    async def seed_all(self):
        try:
            await self.seed_brands()
            await self.seed_colors()
            await self.seed_catalog_hierarchy()

            await self.session.commit()
            logger.info("🚀 All data seeded successfully!")
        except Exception as e:
            await self.session.rollback()
            logger.error(f"❌ Seeding failed: {e}")
            raise


async def main():
    db_settings = PostgresSettings()
    engine = create_async_engine(url=db_settings.database_url, echo=False)
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    async with session_factory() as session:
        seeder = DataSeeder(session)
        await seeder.seed_all()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
