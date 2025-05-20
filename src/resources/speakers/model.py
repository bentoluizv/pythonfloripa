from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.resources import Base
from src.utils import generate_ulid


class Speaker(Base):
    __tablename__ = 'speakers'

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=generate_ulid,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    linkedin_url: Mapped[str] = mapped_column(String(255), nullable=True)
    github_url: Mapped[str] = mapped_column(String(255), nullable=True)
    twitter_url: Mapped[str] = mapped_column(String(255), nullable=True)
    website_url: Mapped[str] = mapped_column(String(255), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    talks: Mapped[list['Talk']] = relationship(back_populates='speaker', lazy='selectin')  # type: ignore  # noqa: F821
