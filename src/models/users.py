from typing import NewType
from uuid import UUID

from sqlalchemy import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

UserId = NewType("UserId", UUID)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    stars: Mapped[int] = mapped_column(INTEGER, nullable=False)
    comment: Mapped[str] = mapped_column(
        VARCHAR(512),
        nullable=True,
    )
