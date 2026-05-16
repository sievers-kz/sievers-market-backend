from src.core.media.domain.value_objects import MediaSize
from src.core.media.infrastructure.models import Media as ORMMedia
from src.core.media.domain.entities import Media as DomainMedia


class MediaMapper:
    @staticmethod
    def to_domain(media: list[ORMMedia]) -> list[DomainMedia]:
        return [
            DomainMedia(
                id=m.id,
                owner_id=m.owner_id,
                media_url=m.media_url,
                media_type=m.media_type,
                media_size=MediaSize(m.media_size),
            ) for m in media
        ]

    @staticmethod
    def to_orm(media: list[DomainMedia]) -> list[ORMMedia]:
        return [
            ORMMedia(
                id=m.id,
                owner_id=m.owner_id,
                media_url=m.media_url,
                media_type=m.media_type,
                media_size=m.media_size.value,
            ) for m in media
        ]
