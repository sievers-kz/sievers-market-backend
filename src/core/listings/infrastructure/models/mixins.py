from sqlalchemy import Text, Computed, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class SearchMixin:
    search_content: Mapped[str | None] = mapped_column(Text, nullable=True)

    @declared_attr
    def search_vector(cls) -> Mapped[TSVECTOR]:
        return mapped_column(
            TSVECTOR,
            Computed(
                "to_tsvector('russian', coalesce(search_content, ''))",
                persisted=True
            )
        )

    @declared_attr
    def __table_args__(cls):
        return (
            Index(
                f"idx_{cls.__tablename__}_vector",
                "search_vector",
                postgresql_using="gin"
            ),
            Index(
                f"idx_{cls.__tablename__}_trgm",
                "search_content",
                postgresql_using="gist",
                postgresql_ops={"search_content": "gist_trgm_ops"}
            )
        )