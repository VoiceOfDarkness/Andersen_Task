from contextlib import AbstractAsyncContextManager
from typing import Callable
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.exceptions import ObjectNotFoundException
from app.models.base import Base


class BaseRepository[Model: Base, CreateSchema: BaseModel, UpdateSchema: BaseModel]:
    def __init__(self,
                 session_factory: Callable[[], AbstractAsyncContextManager[AsyncSession]], model_class: type[Model]):
        self.session_factory = session_factory
        self.model_class = model_class

    async def get_all(self):
        async with self.session_factory() as session:
            stmt = select(self.model_class)
            records = await session.execute(stmt)
            return records.scalars().all()

    async def get(self, id: UUID):
        async with self.session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id)
            record = await session.execute(stmt)
            record = record.scalars().first()
            if record is None:
                raise ObjectNotFoundException(self.model_class.__name__, id)

            return record

    async def create(self, data: CreateSchema):
        async with self.session_factory() as session:
            async with session.begin():
                db_obj = self.model_class(**data.model_dump())
                session.add(db_obj)
                await session.flush()
                return db_obj

    async def update(self, id: UUID, data: UpdateSchema):
        async with self.session_factory() as session:
            async with session.begin():
                stmt = select(self.model_class).where(self.model_class.id == id).with_for_update()
                record = await session.execute(stmt)
                obj = record.scalars().one_or_none()

                if obj is None:
                    raise ObjectNotFoundException(self.model_class.__name__, id)

                update_data = data.model_dump(exclude_unset=True, exclude_none=True)
                for field, val in update_data.items():
                    setattr(obj, field, val)

                await session.flush()
                return obj

    async def delete(self, id: UUID):
        async with self.session_factory() as session:
            async with session.begin():
                stmt = select(self.model_class).where(self.model_class.id == id).with_for_update()
                record = await session.execute(stmt)
                record = record.scalars().one_or_none()

                if record is None:
                    raise ObjectNotFoundException(self.model_class.__name__, id)

                await session.delete(record)
