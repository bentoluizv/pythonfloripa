from typing import Annotated, Optional

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.ext.database.db import get_async_session
from src.resources.shared.schemas import PaginationParams
from src.resources.users.model import User, UserProfile
from src.resources.users.schema import (
    UserCreate,
    UserPublic,
    UsersPaginatedResponse,
    UserUpdate,
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


class UserRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    async def create(self, user_data: UserCreate):
        """Create a new user and return the public schema."""
        # Create User model instance
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=pwd_context.hash(user_data.password),
        )

        # Create profile if provided
        if user_data.profile:
            profile = UserProfile(
                full_name=user_data.profile.full_name,
                linkedin_url=user_data.profile.linkedin_url,
                github_url=user_data.profile.github_url,
                phone_number=user_data.profile.phone_number,
                bio=user_data.profile.bio,
            )
            user.profile = profile

        # Add to session and commit
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: str):
        """Get a user by ID."""

        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, user_id: str, user_data: UserUpdate):
        """Update a user and return the public schema."""
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        # Update user fields
        update_data = user_data.model_dump(exclude_unset=True, exclude={'profile'})
        for field, value in update_data.items():
            if field == 'password':
                setattr(user, 'hashed_password', pwd_context.hash(value))
            else:
                setattr(user, field, value)

        # Update profile if provided
        if user_data.profile:
            profile_data = user_data.profile.model_dump(exclude_unset=True)
            if user.profile:
                # Update existing profile
                for field, value in profile_data.items():
                    setattr(user.profile, field, value)
            else:
                # Create new profile
                profile = UserProfile(**profile_data)
                user.profile = profile

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: str) -> Optional[User]:
        """Delete a user."""
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        await self.session.delete(user)
        await self.session.commit()
        return user

    async def list_users(self, params: PaginationParams) -> UsersPaginatedResponse:
        """List users with pagination."""
        # Get total count efficiently
        count_query = select(func.count()).select_from(User)
        total = await self.session.scalar(count_query) or 0

        # Get paginated users
        query = select(User).offset((params.page - 1) * params.per_page).limit(params.per_page)
        result = await self.session.execute(query)
        users = result.scalars().all()

        # Calculate total pages
        total_pages = (total + params.per_page - 1) // params.per_page

        # Convert to public schemas
        items = [UserPublic.model_validate(user) for user in users]

        return UsersPaginatedResponse(
            total=total,
            page=params.page,
            per_page=params.per_page,
            total_pages=total_pages,
            items=items,
        )


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserRepository:
    """
    Dependency that provides a UserRepository instance.
    """
    return UserRepository(session)
