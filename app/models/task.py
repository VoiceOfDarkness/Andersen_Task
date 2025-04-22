import uuid
from enum import Enum as PyEnum
from typing import Annotated, Optional

from sqlalchemy import UUID, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, Relationship, mapped_column

from app.models.base import Base


class TaskStatus(str, PyEnum):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Annotated[TaskStatus, "Current status of task"]] = mapped_column(Enum(TaskStatus),
                                                                                    default=TaskStatus.NEW)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = Relationship(back_populates="tasks")  # noqa
