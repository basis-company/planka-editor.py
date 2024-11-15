from datetime import datetime
from typing import Optional

from sqlalchemy import func, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class UserAccount(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default=func.next_id()
    )
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)
    organization: Mapped[Optional[str]] = mapped_column(Text)
    subscribe_to_own_cards: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
    deleted_at: Mapped[Optional[datetime]]
    language: Mapped[Optional[str]] = mapped_column(Text)
    password_changed_at: Mapped[Optional[datetime]]
    avatar: Mapped[Optional[dict]] = mapped_column(JSONB)
    is_sso: Mapped[bool] = mapped_column(Boolean, nullable=False)
