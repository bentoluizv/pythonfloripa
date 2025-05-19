from fastapi.params import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing_extensions import Annotated

from src.ext.database.db import get_async_session
from src.resources.events.model import Event
from src.resources.shared.schemas import PaginationParams
from src.resources.talks.model import Talk
from src.resources.talks.schema import TalkCreate, TalkUpdate


class TalkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, talk_data: TalkCreate):
        talk = Talk(
            title=talk_data.title,
            description=talk_data.description,
            speaker=talk_data.speaker,
            start_time=talk_data.start_time,
            end_time=talk_data.end_time,
            event_id=talk_data.event_id,
        )

        self.session.add(talk)

        await self.session.commit()
        await self.session.refresh(talk)

        return talk

    async def get_by_id(self, talk_id: str):
        query = select(Talk).where(Talk.id == talk_id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_event_edition(self, event_edition: int):
        query = select(Talk).join(Talk.event).where(Event.edition == event_edition).options(selectinload(Talk.event))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, talk_id: str, talk_data: TalkUpdate):
        talk = await self.get_by_id(talk_id)

        if talk is None:
            return None

        update_data = talk_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(talk, field, value)

        await self.session.commit()
        await self.session.refresh(talk)

        return talk

    async def delete(self, talk_id: str):
        talk = await self.get_by_id(talk_id)

        if talk is None:
            return None

        await self.session.delete(talk)
        await self.session.commit()

        return talk

    async def list_talks(self, params: PaginationParams):
        count_query = select(func.count()).select_from(Talk)
        total = await self.session.scalar(count_query) or 0

        query = select(Talk).offset((params.page - 1) * params.per_page).limit(params.per_page)
        result = await self.session.execute(query)
        talks = result.scalars().all()

        total_pages = (total + params.per_page - 1) // params.per_page

        return {
            'total': total,
            'page': params.page,
            'per_page': params.per_page,
            'total_pages': total_pages,
            'items': talks,
        }


def get_talk_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> TalkRepository:
    """
    Dependency that provides a TalkRepository instance.
    """
    return TalkRepository(session)
