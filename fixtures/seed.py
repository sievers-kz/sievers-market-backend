import json
import logging
from pathlib import Path
from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.configuration.settings.settings import PostgresSettings
from src.core.references.infrastructure.models import (
    Country,
    Brand,
    Color,
    UnitOfMeasure,
    Region,
    City,
    Rubric,
    Category,
    Subcategory,
    Attribute,
    AttributeOption,
    AttrGroup,
    SubcategoryAttribute
)
from src.core.references.domain.enums import AttrValueType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSeeder:
    """Класс для заполнения БД reference данными"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.fixtures_path = Path("fixtures/data")

    def _load_json(self, filename: str) -> Any:
        """Загружает JSON файл из fixtures/data"""
        filepath = self.fixtures_path / filename
        logger.info(f"Loading {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    async def seed_countries(self):
        """Заполняет таблицу стран"""
        logger.info("🌍 Seeding countries...")
        data = self._load_json("countries.json")

        for item in data:
            country = Country(name=item["name"])
            self.session.add(country)

        await self.session.commit()
        logger.info("✅ Countries seeded")

    async def seed_brands(self):
        """Заполняет таблицу брендов"""
        logger.info("🏭 Seeding brands...")
        data = self._load_json("brands.json")

        for item in data:
            brand = Brand(name=item["name"])
            self.session.add(brand)

        await self.session.commit()
        logger.info("✅ Brands seeded")

    async def seed_colors(self):
        """Заполняет таблицу цветов"""
        logger.info("🎨 Seeding colors...")
        data = self._load_json("colors.json")

        for item in data:
            color = Color(name=item["name"], hex=item["hex"])
            self.session.add(color)

        await self.session.commit()
        logger.info("✅ Colors seeded")

    async def seed_unit_of_measures(self):
        """Заполняет таблицу единиц измерения"""
        logger.info("📏 Seeding units of measure...")
        data = self._load_json("uom.json")

        for item in data:
            uom = UnitOfMeasure(name=item["name"], label=item["label"])
            self.session.add(uom)

        await self.session.commit()
        logger.info("✅ Units of measure seeded")

    async def seed_regions_and_cities(self):
        """Заполняет регионы и города (с FK связью)"""
        logger.info("🏙️ Seeding regions and cities...")
        data = self._load_json("regions.json")

        for region_name, cities in data.items():
            region = Region(name=region_name)
            self.session.add(region)
            await self.session.flush()

            for city_name in cities:
                city = City(name=city_name, region_id=region.id)
                self.session.add(city)

        await self.session.commit()
        logger.info("✅ Regions and cities seeded")

    async def seed_categories_hierarchy(self):
        """
        Заполняет иерархию: Rubric → Category → Subcategory

        Формат JSON:
        {
          "Техника": {
            "Тракторы": ["Колесные тракторы", "Гусеничные тракторы"],
            "Комбайны": ["Зерноуборочные", "Кормоуборочные"]
          }
        }
        """
        logger.info("📦 Seeding categories hierarchy...")
        data = self._load_json("categories.json")

        for rubric_name, categories_dict in data.items():
            rubric = Rubric(name=rubric_name)
            self.session.add(rubric)
            await self.session.flush()

            for category_name, subcategory_list in categories_dict.items():
                category = Category(name=category_name, rubric_id=rubric.id)
                self.session.add(category)
                await self.session.flush()

                for subcategory_name in subcategory_list:
                    subcategory = Subcategory(name=subcategory_name, category_id=category.id)
                    self.session.add(subcategory)

        await self.session.commit()
        logger.info("✅ Categories hierarchy seeded")

    async def seed_attributes(self):
        """
        Заполняет атрибуты (опционально с группами и опциями)

        Формат JSON:
        [
          {
            "key": "engine_power",
            "label": "Мощность двигателя",
            "value_type": "float",
            "group": "Двигатель",  // опционально
            "options": [           // опционально для enum
              {"key": "diesel", "label": "Дизель"},
              {"key": "petrol", "label": "Бензин"}
            ]
          }
        ]
        """
        logger.info("⚙️ Seeding attributes...")
        data = self._load_json("attributes.json")

        for item in data:
            attribute = Attribute(
                key=item["key"],
                label=item["label"],
                value_type=AttrValueType(item["value_type"]),
            )

            self.session.add(attribute)
            await self.session.flush()

            if "options" in item and item["options"]:
                for option in item["options"]:
                    attr_option = AttributeOption(
                        attribute_id=attribute.id,
                        key=option["key"],
                        label=option["label"]
                    )
                    self.session.add(attr_option)

        await self.session.commit()
        logger.info("✅ Attributes seeded")

    async def link_attributes_to_subcategories(self):
        """
        Связывает атрибуты с подкатегориями через SubcategoryAttribute

        Можно создать JSON файл с маппингом:
        {
          "Колесные тракторы": [
            {"attribute": "engine_power", "unit": "h.p", "required": true, "filterable": true},
            {"attribute": "max_speed", "unit": "km/h", "required": false, "filterable": true}
          ]
        }
        """
        logger.info("🔗 Linking attributes to subcategories...")
        data = self._load_json("subcategory_attributes.json")

        result = await self.session.execute(select(Subcategory))
        subcategories = {s.name: s for s in result.scalars().all()}

        result = await self.session.execute(select(Attribute))
        attributes = {a.key: a for a in result.scalars().all()}

        result = await self.session.execute(select(UnitOfMeasure))
        units = {u.name: u for u in result.scalars().all()}

        for subcategory_name, attr_configs in data.items():
            if subcategory_name not in subcategories:
                logger.warning(f"⚠️ Subcategory '{subcategory_name}' not found, skipping")
                continue

            subcategory = subcategories[subcategory_name]

            for config in attr_configs:
                attr_key = config["attribute"]

                if attr_key not in attributes:
                    logger.warning(f"⚠️ Attribute '{attr_key}' not found, skipping")
                    continue

                attribute = attributes[attr_key]

                unit_id = None
                if "unit" in config and config["unit"]:
                    unit_name = config["unit"]
                    if unit_name in units:
                        unit_id = units[unit_name].id
                    else:
                        logger.warning(f"⚠️ Unit '{unit_name}' not found")

                subcategory_attr = SubcategoryAttribute(
                    subcategory_id=subcategory.id,
                    attribute_id=attribute.id,
                    unit_id=unit_id,
                    is_required=config.get("required", False),
                    is_filterable=config.get("filterable", False)
                )
                self.session.add(subcategory_attr)

        await self.session.commit()
        logger.info("✅ Attributes linked to subcategories")

    async def seed_all(self):
        """Запускает все seed функции в правильном порядке"""
        logger.info("🚀 Starting database seeding...")

        try:
            # 1. Простые справочники (без FK)
            await self.seed_countries()
            await self.seed_brands()
            await self.seed_colors()
            await self.seed_unit_of_measures()

            await self.seed_regions_and_cities()
            await self.seed_categories_hierarchy()
            await self.seed_attributes()
            await self.link_attributes_to_subcategories()

            logger.info("✅ Database seeded successfully!")

        except Exception as e:
            logger.error(f"❌ Error seeding database: {e}")
            await self.session.rollback()
            raise


async def main():
    """Entry point для запуска seed"""
    db_settings = PostgresSettings()
    engine = create_async_engine(url=db_settings.database_url, echo=False)
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    async with session_factory() as session:
        seeder = DataSeeder(session)
        await seeder.seed_all()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
