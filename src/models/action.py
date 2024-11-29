from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Action(Base):
    __tablename__ = 'action'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
    card_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
