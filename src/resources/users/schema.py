from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, constr, field_validator

from src.resources.shared.schemas import BasePaginatedResponse
from src.utils import validade_password

# Custom validators
PhoneNumber = Annotated[str, constr(pattern=r'^\+[1-9]\d{1,14}$')]
LinkedInUrl = Annotated[str, constr(pattern=r'^https://linkedin\.com/in/[\w-]+$')]
GithubUrl = Annotated[str, constr(pattern=r'^https://github\.com/[\w-]+$')]


class UserProfile(BaseModel):
    """Base schema for user profile data."""

    full_name: Optional[str] = Field(None, max_length=100)
    linkedin_url: Optional[LinkedInUrl] = Field(None, max_length=255)
    github_url: Optional[GithubUrl] = Field(None, max_length=255)
    phone_number: Optional[PhoneNumber] = Field(None, max_length=255)
    bio: Optional[str] = Field(None, max_length=500)


class UserProfileInDB(UserProfile):
    """Schema for user profile data from database."""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Base schema for user data."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8)
    profile: Optional[UserProfile] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """Validate password complexity."""
        if v is None:
            return v
        return validade_password(v)


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    profile: Optional[UserProfile] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """Validate password complexity."""
        if v is None:
            return v
        return validade_password(v)


class UserInDB(UserBase):
    """Schema for user data from database."""

    id: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    profile: Optional[UserProfileInDB] = None

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    """Schema for public user data."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'id': '01HGD7XQZ8K3N4P5R6S7T8U9V0',
                'email': 'usuario@exemplo.com',
                'username': 'usuario123',
                'is_active': True,
                'is_superuser': False,
                'created_at': '2024-03-20T10:00:00',
                'updated_at': '2024-03-20T10:00:00',
                'profile': {
                    'id': '01HGD7XQZ8K3N4P5R6S7T8U9V1',
                    'user_id': '01HGD7XQZ8K3N4P5R6S7T8U9V0',
                    'full_name': 'Usuário Exemplo',
                    'linkedin_url': 'https://linkedin.com/in/usuario',
                    'github_url': 'https://github.com/usuario',
                    'phone_number': '+5511999999999',
                    'bio': 'Desenvolvedor Python',
                    'created_at': '2024-03-20T10:00:00',
                    'updated_at': '2024-03-20T10:00:00',
                },
            }
        },
    )
    id: str
    email: EmailStr
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    profile: Optional[UserProfile] = None


class UsersPaginatedResponse(BasePaginatedResponse):
    """Schema for paginated response of users."""

    items: List[UserPublic]
