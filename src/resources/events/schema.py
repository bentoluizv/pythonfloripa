from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.resources.shared.schemas import BasePaginatedResponse


class EventDB(BaseModel):
    """Schema for event data from database."""

    id: str
    edition: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    image_url: str
    is_active: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    """Schema for creating an event."""

    edition: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    image_url: str


class EventUpdate(BaseModel):
    """Schema for updating an event."""

    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None


class EventsPaginatedResponse(BasePaginatedResponse):
    items: List[EventDB]
