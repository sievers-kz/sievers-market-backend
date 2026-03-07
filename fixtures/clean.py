import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.configuration.settings.settings import PostgresSettings
from src.core.references.infrastructure.models import (
    SubcategoryAttribute, AttributeOption, Attribute,
    Subcategory, Category, Rubric, City, Region,
    Color, UnitOfMeasure, Brand, Country
)


async def clean_all():
    db_settings = PostgresSettings()
    engine = create_async_engine(url=db_settings.database_url, echo=False)
    session_factory = async_sessionmaker(bind=engine, autoflush=False)

    async with session_factory() as session:
        tables = [
            SubcategoryAttribute,
            AttributeOption,
            Attribute,
            Subcategory,
            Category,
            Rubric,
            City,
            Region,
            Color,
            UnitOfMeasure,
            Brand,
            Country
        ]

        for table in tables:
            await session.execute(table.__table__.delete())
            print(f"✅ Cleared {table.__tablename__}")

        await session.commit()
        print("🎉 All seed data cleaned!")


if __name__ == "__main__":
    asyncio.run(clean_all())