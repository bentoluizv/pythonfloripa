from typing import Annotated

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.ext.database.db import get_async_session
from src.resources.events.model import Event
from src.resources.events.schema import EventCreate, EventUpdate
from src.resources.shared.schemas import PaginationParams

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


class EventRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    async def create(self, event_data: EventCreate):
        event = Event(
            edition=event_data.edition,
            title=event_data.title,
            description=event_data.description,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            location=event_data.location,
            image_url=event_data.image_url,
        )

        self.session.add(event)

        await self.session.commit()
        await self.session.refresh(event)

        return event

    async def get_by_id(self, event_id: str):
        query = select(Event).where(Event.id == event_id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_edition(self, edition: int):
        query = select(Event).where(Event.edition == edition)
        result = await self.session.execute(query)

        return result.scalars().first()

    async def update(self, event_id: str, event_data: EventUpdate):
        event = await self.get_by_id(event_id)

        if event is None:
            return None

        update_data = event_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(event, field, value)

        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete(self, event_id: str):
        event = await self.get_by_id(event_id)

        if event is None:
            return None

        if event.talks:
            raise Exception('Event has talks')

        await self.session.delete(event)
        await self.session.commit()

        return event

    async def list_events(self, params: PaginationParams):
        count_query = select(func.count()).select_from(Event)
        total = await self.session.scalar(count_query) or 0

        query = select(Event).offset((params.page - 1) * params.per_page).limit(params.per_page)
        result = await self.session.execute(query)
        events = result.scalars().all()

        total_pages = (total + params.per_page - 1) // params.per_page

        return {
            'total': total,
            'page': params.page,
            'per_page': params.per_page,
            'total_pages': total_pages,
            'items': events,
        }


def get_event_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> EventRepository:
    """
    Dependency that provides a EventRepository instance.
    """
    return EventRepository(session)
