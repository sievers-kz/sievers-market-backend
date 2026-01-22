import logging

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
    Subcategory
)


RUBRICS = ["Техника", "Животноводство", "Запчасти", "Недвижимость", "Услуги"]

CATEGORIES = {
    "Тракторы": ["Колёсные тракторы", "Гусеничные тракторы", "Мини-тракторы"],
    "Комбайны": ["Зерноуборочные комбайны", "Кормоуборочные комбайны"],
    "Автотранспорт": ["Грузовой автотранспорт", "Легковой автотранспорт"]
}

REGIONS = {
    "Павлодарская область": ["Павлодар", "Экибастуз", "Аксу"],
    "Акмолинская область": ["Астана", "Косшы", "Ерейментау"],
    "Алматинская область": ["Алматы", "Конаев", "Талдыкорган"],
}

COUNTRIES = ["Россия", "Казахстан", "США", "Германия", "Япония", "Китай", "Беларусь"]

UOM = [
    {"name": "h.p", "label": "л.с"},
    {"name": "kg", "label": "кг"},
    {"name": "h", "label": "ч"},
    {"name": "m", "label": "м"},
    {"name": "mm", "label": "мм"},
    {"name": "cm", "label": "см"},
]

BRANDS = ["John Deere", "New Holland", "CASE IH", "Rostselmash", "Belarus", "Deutz Fahr", "Fendt"]

COLORS = [
    {"name": "Красный", "hex": "FF0000"},
    {"name": "Белый", "hex": "FFFFFF"},
    {"name": "Черный", "hex": "000000"}
]


logger = logging.getLogger(__name__)


async def seed_simple_tables(session: AsyncSession):
    """Заполняет простые справочники без FK"""

    # 1. Страны
    for name in COUNTRIES:
        exists = await session.scalar(select(Country).where(Country.name == name))
        if not exists:
            session.add(Country(name=name))

    # 2. Бренды
    for name in BRANDS:
        exists = await session.scalar(select(Brand).where(Brand.name == name))
        if not exists:
            session.add(Brand(name=name))

    # 3. Цвета
    for item in COLORS:
        exists = await session.scalar(select(Color).where(Color.name == item["name"]))
        if not exists:
            session.add(Color(name=item["name"], hex=item["hex"]))

    # 4. Единицы измерения
    for item in UOM:
        exists = await session.scalar(select(UnitOfMeasure).where(UnitOfMeasure.name == item["name"]))
        if not exists:
            session.add(UnitOfMeasure(name=item["name"], label=item["label"]))

    await session.commit()
    logger.info("Simple tables seeded.")


async def seed_geo(session: AsyncSession):
    """Заполняет Регионы и Города"""
    for reg_name, cities in REGIONS.items():
        # Ищем или создаем Регион
        region = await session.scalar(select(Region).where(Region.name == reg_name))
        if not region:
            region = Region(name=reg_name)
            session.add(region)
            await session.flush()  # Чтобы получить region.id

        # Создаем города
        for city_name in cities:
            exists = await session.scalar(select(City).where(City.name == city_name))
            if not exists:
                session.add(City(name=city_name, region_id=region.id))

    await session.commit()
    logger.info("Geo seeded.")


async def seed_rubrics_and_categories(session: AsyncSession):
    """Заполняет Рубрики -> Категории -> Подкатегории"""

    # 1. Создаем Рубрики
    rubric_map = {}
    for name in RUBRICS:
        rubric = await session.scalar(select(Rubric).where(Rubric.name == name))
        if not rubric:
            rubric = Rubric(name=name)
            session.add(rubric)
            await session.flush()
        rubric_map[name] = rubric

    # 2. Заполняем "Технику" (Machinery)
    tech_rubric = rubric_map.get("Техника")
    if tech_rubric:
        for cat_name, subcats in CATEGORIES.items():
            # Категория
            category = await session.scalar(select(Category).where(Category.name == cat_name))
            if not category:
                category = Category(name=cat_name, rubric_id=tech_rubric.id)
                session.add(category)
                await session.flush()

            # Подкатегории
            for sub_name in subcats:
                exists = await session.scalar(select(Subcategory).where(Subcategory.name == sub_name))
                if not exists:
                    session.add(Subcategory(name=sub_name, category_id=category.id))

    await session.commit()
    logger.info("Rubrics structure seeded.")


async def main():
    db_settings = PostgresSettings()
    engine = create_async_engine(url=db_settings.database_url)
    session_factory = async_sessionmaker(bind=engine, autoflush=False)

    async with session_factory() as session:
        try:
            await seed_simple_tables(session)
            await seed_geo(session)
            await seed_rubrics_and_categories(session)
            print("✅ Database seeded successfully!")
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            await session.rollback()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
