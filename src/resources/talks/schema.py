from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.resources.shared.schemas import BasePaginatedResponse


class TalkDB(BaseModel):
    id: str
    title: str
    description: str
    speaker: str
    start_time: datetime
    end_time: datetime
    event_id: str
    event: 'EventDB'  # type: ignore  # noqa: F821
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicTalk(BaseModel):
    id: str
    title: str
    speaker: str
    start_time: datetime
    end_time: datetime
    event: 'PublicEvent'  # type: ignore  # noqa: F821


class TalkCreate(BaseModel):
    title: str
    description: str
    speaker: str
    start_time: datetime
    end_time: datetime
    event_id: str


class TalkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    speaker: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    event_id: Optional[str] = None


class TalksPaginatedResponse(BasePaginatedResponse):
    items: List[TalkDB]
