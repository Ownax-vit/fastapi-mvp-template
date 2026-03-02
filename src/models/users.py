from typing import NewType
from uuid import UUID

from sqlalchemy import INTEGER, VARCHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.types import Gender

UserId = NewType("UserId", UUID)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    gender: Mapped[str] = mapped_column(
        Enum(Gender), nullable=False, server_default=Gender.unknown
    )
    stars: Mapped[int] = mapped_column(INTEGER, nullable=False)
    comment: Mapped[str] = mapped_column(
        VARCHAR(512),
        nullable=True,
    )
