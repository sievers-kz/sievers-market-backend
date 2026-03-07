from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.machinery.infrastructure.models import Machinery


class Wishlist(BaseModel):
    __tablename__ = "wishlist"

    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    machinery_id: Mapped[UUID] = mapped_column(ForeignKey("machinery.id", ondelete="CASCADE"), nullable=False)
    machinery: Mapped["Machinery"] = relationship()

    __table_args__ = (
        UniqueConstraint('customer_id', 'machinery_id', name='uq_wishlist_customer_machinery'),
    )
