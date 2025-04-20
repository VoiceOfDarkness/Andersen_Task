import uuid
from enum import Enum as PyEnum
from typing import Optional, Annotated

from sqlalchemy.orm import Mapped, mapped_column, Relationship
from sqlalchemy import String, UUID, Text, Enum, ForeignKey

from .base import Base


class TaskStatus(str, PyEnum):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Annotated[TaskStatus, "Current status of task"]] = mapped_column(Enum(TaskStatus),
                                                                                    default=TaskStatus.NEW)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = Relationship(back_populates="tasks")