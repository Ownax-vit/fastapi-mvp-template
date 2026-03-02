from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, Field

from src.models.types import Gender
from src.schemas.base import Base, BasePagination


class UserBase(Base):
    name: str = Field(..., description="user name")
    stars: int = Field(..., description="stars")
    comment: str = Field(..., description="comment")
    gender: Gender = Field(..., description="gender")

    model_config = ConfigDict(title="USER BASE")


class UserIn(UserBase): ...


class User(UserBase):
    id: UUID = Field(..., description="ID USER")
    created_at: datetime = Field(..., description="created at")


class UserPagination(BasePagination):
    items: list[User] = Field(default_factory=list, description="The list of users")
    model_config = ConfigDict(title="USER PAGINATION")
