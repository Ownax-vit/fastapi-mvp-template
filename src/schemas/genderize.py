from enum import StrEnum

from pydantic import Field

from src.schemas.base import Base


class GenderizeGender(StrEnum):
    female = "female"
    male = "male"


class GenderizeResponse(Base):
    count: int = Field(
        ...,
    )
    name: str = Field(
        ...,
    )
    country_id: str = Field(
        ...
    )
    gender: GenderizeGender = Field(
        ...
    )
    probability: float = Field(
        ...
    )
