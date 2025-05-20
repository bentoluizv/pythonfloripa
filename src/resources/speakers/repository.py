from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.ext.database.db import get_async_session
from src.resources.shared.schemas import PaginationParams
from src.resources.speakers.model import Speaker
from src.resources.speakers.schema import SpeakerCreate, SpeakerUpdate


class SpeakerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, speaker_data: SpeakerCreate):
        speaker = Speaker(
            name=speaker_data.name,
            email=speaker_data.email,
            linkedin_url=speaker_data.linkedin_url,
            github_url=speaker_data.github_url,
            twitter_url=speaker_data.twitter_url,
            website_url=speaker_data.website_url,
            bio=speaker_data.bio,
            image_url=speaker_data.image_url,
        )

        self.session.add(speaker)

        await self.session.commit()
        await self.session.refresh(speaker)

        return speaker

    async def get_by_id(self, speaker_id: str):
        query = select(Speaker).where(Speaker.id == speaker_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        query = select(Speaker).where(Speaker.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, speaker_id: str, speaker_data: SpeakerUpdate):
        speaker = await self.get_by_id(speaker_id)

        if speaker is None:
            return None

        update_data = speaker_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(speaker, field, value)

        await self.session.commit()
        await self.session.refresh(speaker)

        return speaker

    async def delete(self, speaker_id: str):
        speaker = await self.get_by_id(speaker_id)

        if speaker is None:
            return None

        await self.session.delete(speaker)
        await self.session.commit()

    async def list_speakers(self, params: PaginationParams):
        count_query = select(func.count()).select_from(Speaker)
        total = await self.session.scalar(count_query) or 0

        query = select(Speaker).offset((params.page - 1) * params.per_page).limit(params.per_page)
        result = await self.session.execute(query)

        speakers = result.scalars().all()

        total_pages = (total + params.per_page - 1) // params.per_page

        return {
            'total': total,
            'page': params.page,
            'per_page': params.per_page,
            'total_pages': total_pages,
            'items': speakers,
        }


def get_speaker_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SpeakerRepository:
    """
    Dependency that provides a SpeakerRepository instance.
    """
    return SpeakerRepository(session)
