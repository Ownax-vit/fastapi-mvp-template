from math import ceil

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
)
from pydantic.alias_generators import to_camel


class Base(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
        alias_generator=to_camel,
        validate_by_name=True,
    )


class BasePagination(Base):
    page: int = Field(default=1, description="The page number", ge=1)
    per_page: int = Field(default=10, description="The number of items per page", ge=1)
    total: int = Field(default=0, description="The total number of items")
    cursor: str | None = Field(
        default=None, description="Current position of the cursor"
    )

    @property
    @computed_field
    def total_pages(self) -> int:
        return ceil(self.total / self.per_page)

    @property
    @computed_field
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @field_validator("page", mode="before")
    @classmethod
    def validate_page(cls, value: int, info: ValidationInfo) -> int:
        if value > 1 and value > info.data["total_pages"]:
            # TODO починить
            value = info.data["total_pages"]
        return value
