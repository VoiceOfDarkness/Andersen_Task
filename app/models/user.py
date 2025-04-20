import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Text

from models.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped["Task"] = relationship(back_populates="user", cascade="all, delete-orphan")
