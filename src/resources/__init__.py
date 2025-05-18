from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from src.resources.events import model as events_model  # noqa: E402, F401
from src.resources.users import model as users_model  # noqa: E402, F401

__all__ = ['Base']
