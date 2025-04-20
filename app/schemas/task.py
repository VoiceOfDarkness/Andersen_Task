from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(...)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.NEW)


class TaskCreate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: UUID
    user_id: UUID
