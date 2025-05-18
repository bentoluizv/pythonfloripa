from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from src.resources.users import model as users_model  # noqa: E402, F401

__all__ = ['Base']
