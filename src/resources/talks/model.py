from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.resources import Base
from src.utils import generate_ulid


class Talk(Base):
    __tablename__ = 'talks'

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=generate_ulid,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    event_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('events.id', ondelete='RESTRICT'),
        nullable=False,
    )
    event: Mapped['Event'] = relationship(back_populates='talks', lazy='joined')  # type: ignore # noqa: F821
    speaker_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('speakers.id', ondelete='RESTRICT'),
        nullable=False,
    )
    speaker: Mapped['Speaker'] = relationship(back_populates='talks', lazy='joined')  # type: ignore # noqa: F821
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )
