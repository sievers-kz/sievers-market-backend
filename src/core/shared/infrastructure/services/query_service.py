import math

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.shared.presentation.dto import DTO


class QueryService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def paginate(
        self,
        statement,
        schema: type[DTO],
        page: int,
        limit: int,
    ) -> DTO:
        count_stmt = select(func.count()).select_from(statement.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        paginated = statement.limit(limit).offset((page - 1) * limit)
        results = (await self._session.execute(paginated)).mappings().all()

        return {
            "items": [schema.model_validate(result) for result in results],
            "total": total,
            "page": page,
            "pages": math.ceil(total / limit),
        }
