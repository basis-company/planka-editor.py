from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Label(Base):
    __tablename__ = 'label'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
    board_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str]
    color: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
    position: Mapped[float] = mapped_column(nullable=False)
