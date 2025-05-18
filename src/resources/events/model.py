from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.resources import Base
from src.resources.talks.model import Talk
from src.utils import generate_ulid


class Event(Base):
    """Event model for SQLAlchemy."""

    __tablename__ = 'events'

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=generate_ulid,
    )

    edition: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    talks: Mapped[List[Talk]] = relationship(back_populates='event', lazy='selectin')  # type: ignore  # noqa: F821
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
