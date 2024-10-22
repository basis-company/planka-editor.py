from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
    name: Mapped[str] = mapped_column(nullable=False)
    background: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
    background_image: Mapped[Optional[dict]] = mapped_column(JSONB)
