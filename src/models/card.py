from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Card(Base):
    __tablename__ = 'card'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
    board_id: Mapped[int] = mapped_column(nullable=False)
    list_id: Mapped[int] = mapped_column(nullable=False)
    creator_user_id: Mapped[int] = mapped_column(nullable=False)
    cover_attachment_id: Mapped[Optional[int]]
    position: Mapped[Optional[float]]
    name: Mapped[str]
    description: Mapped[Optional[str]]
    due_date: Mapped[Optional[datetime]]
    stopwatch: Mapped[Optional[JSON]]
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
    is_due_date_completed: Mapped[Optional[bool]]
