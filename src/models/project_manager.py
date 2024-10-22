from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class ProjectManager(Base):
    __tablename__ = 'project_manager'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
    project_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
