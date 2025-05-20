from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
