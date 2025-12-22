from sqlalchemy.ext.asyncio import AsyncSession


class ListingFormQueryService:
    def __init__(self, session: AsyncSession):
        self._session = session
