from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from ..shared.schemas import BasePaginatedResponse


class SpeakerDB(BaseModel):
    id: str
    name: str
    email: str
    linkedin_url: str
    github_url: str
    twitter_url: str
    website_url: str
    bio: str
    image_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicSpeaker(BaseModel):
    id: str
    name: str
    email: str
    linkedin_url: str
    github_url: str
    twitter_url: str
    website_url: str
    bio: str
    image_url: str


class SpeakerCreate(BaseModel):
    name: str
    email: str
    linkedin_url: str
    github_url: str
    twitter_url: str
    website_url: str
    bio: str
    image_url: str


class SpeakerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twitter_url: Optional[str] = None
    website_url: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None


class SpeakersPaginatedResponse(BasePaginatedResponse):
    items: List[SpeakerDB]
