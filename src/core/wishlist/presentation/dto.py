from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WishlistCard(BaseModel):
    id: UUID
    title: str
    subcategory: str
    price: int
    currency: str
    city: str
    created_at: datetime
