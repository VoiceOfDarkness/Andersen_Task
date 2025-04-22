from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserBase


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


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    user: UserBase


class TaskInDB(TaskBase):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID


class TaskUpdateInDB(TaskUpdate):
    model_config = ConfigDict(from_attributes=True)
    status: Optional[TaskStatus] = Field(default=None)
