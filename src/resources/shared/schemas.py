from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""

    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)


class BasePaginatedResponse(BaseModel):
    """Schema for paginated response."""

    total: int
    page: int
    per_page: int
    total_pages: int
