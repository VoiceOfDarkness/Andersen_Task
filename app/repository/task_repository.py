from app.repository.base_repository import BaseRepository
from uuid import UUID
from app.models.task import Task
from app.schemas.task import TaskInDB, TaskUpdateInDB
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.core.exceptions import ObjectNotFoundException


class TaskRepository(BaseRepository[Task, TaskInDB, TaskUpdateInDB]):
    def __init__(self, session_factory):
        super().__init__(session_factory, Task)

    async def get_all(self, pagination=None, **filters):
        async with self.session_factory() as session:
            stmt = select(self.model_class).options(selectinload(self.model_class.user))
            if filters.get('status') is not None:
                stmt = stmt.where(self.model_class.status == filters['status'])

            if pagination:
                stmt = stmt.offset(pagination.offset).limit(pagination.page_size)

            records = await session.execute(stmt)
            return records.scalars().all()

    async def get(self, id: UUID):
        async with self.session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id).options(
                selectinload(self.model_class.user))

            record = await session.execute(stmt)
            record = record.scalars().one_or_none()
            if record is None:
                raise ObjectNotFoundException(self.model_class.__name__, id)

            return record

    async def count(self, **filters):
        async with self.session_factory() as session:
            stmt = select(func.count()).select_from(self.model_class)

            if filters.get('status') is not None:
                stmt = stmt.where(self.model_class.status == filters['status'])

            result = await session.execute(stmt)
            return result.scalar()

    async def delete_user_task(self, id: UUID, user_id: UUID):
        async with self.session_factory() as session:
            async with session.begin():
                stmt = select(self.model_class).where(
                    (self.model_class.id == id) & (self.model_class.user_id == user_id)).with_for_update()
                record = await session.execute(stmt)
                record = record.scalars().one_or_none()

                if record is None:
                    raise ObjectNotFoundException(self.model_class.__name__, id)

                await session.delete(record)

    async def update_user_task(self, id: UUID, user_id: UUID, data: TaskInDB):
        async with self.session_factory() as session:
            async with session.begin():
                stmt = select(self.model_class).where(
                    (self.model_class.id == id) & (self.model_class.user_id == user_id)).with_for_update()
                record = await session.execute(stmt)
                obj = record.scalars().one_or_none()

                if obj is None:
                    raise ObjectNotFoundException(self.model_class.__name__, id)

                update_data = data.model_dump(exclude_unset=True, exclude_none=True)
                for field, val in update_data.items():
                    setattr(obj, field, val)

                await session.flush()
                return obj

    async def get_user_task(self, user_id: UUID, pagination=None, **filters):
        async with self.session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.user_id == user_id).options(
                selectinload(self.model_class.user))
            if filters.get('status') is not None:
                stmt = stmt.where(self.model_class.status == filters['status'])

            if pagination:
                stmt = stmt.offset(pagination.offset).limit(pagination.page_size)

            record = await session.execute(stmt)
            record = record.scalars().all()
            if record is None:
                raise ObjectNotFoundException(self.model_class.__name__, id)

            return record
