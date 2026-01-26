from src.core.media.domain.entities import Media as DomainMedia
from src.core.media.infrastructure.models import Media as ORMMedia


class MediaMapper:
    @staticmethod
    def to_domain(media: ORMMedia) -> DomainMedia:
        return [
            DomainMedia(
                id=m.id,
                machinery_id=m.machinery_id,
                media_url=m.media_url,
                media_type=m.media_type,
                media_size=m.media_size,
                position=m.position,
            ) for m in media
        ]

    @staticmethod
    def to_orm(media: DomainMedia) -> ORMMedia:
        return [
            ORMMedia(
                id=m.id,
                machinery_id=m.machinery_id,
                media_url=m.media_url,
                media_type=m.media_type,
                media_size=m.media_size,
                position=m.position,
            ) for m in media
        ]