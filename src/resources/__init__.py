from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from src.resources.events import model as events_model  # noqa: E402, F401
from src.resources.speakers import model as speakers_model  # noqa: E402, F401
from src.resources.talks import model as talks_model  # noqa: E402, F401
from src.resources.users import model as users_model  # noqa: E402, F401

__all__ = ['Base', 'events_model', 'speakers_model', 'talks_model', 'users_model']
