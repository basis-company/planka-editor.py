# from datetime import datetime
# from typing import Optional

from sqlalchemy import func
# from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Attachment(Base):
    __tablename__ = 'attachment'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
