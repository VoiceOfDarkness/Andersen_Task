from typing import List

from pydantic import BaseModel, ConfigDict, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginationResponse[T](BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: List[T] | T
    total: int
    page: int
    page_size: int
    pages: int
