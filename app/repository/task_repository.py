from repository.base_repository import BaseRepository
from uuid import UUID
from models.task import Task
from schemas.task import TaskInDB, TaskUpdateInDB
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from core.exceptions import ObjectNotFoundException


class TaskRepository(BaseRepository[Task, TaskInDB, TaskUpdateInDB]):
    def __init__(self, session_factory):
        super().__init__(session_factory, Task)

    async def get_all(self, pagination=None, **filters):
        async with self.session_factory() as session:
            stmt = select(Task).options(selectinload(Task.user))
            if filters.get('status') is not None:
                stmt = stmt.where(Task.status == filters['status'])

            if pagination:
                stmt = stmt.offset(pagination.offset).limit(pagination.page_size)

            records = await session.execute(stmt)
            return records.scalars().all()

    async def get(self, id: UUID, **filters):
        async with self.session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id).options(selectinload(Task.user))
            if filters.get('status') is not None:
                stmt = stmt.where(Task.status == filters['status'])

            record = await session.execute(stmt)
            record = record.scalars().one_or_none()
            if record is None:
                raise ObjectNotFoundException(self.model_class.__name__, id)

            return record

    async def count(self, **filters):
        async with self.session_factory() as session:
            stmt = select(func.count()).select_from(self.model_class)

            if filters.get('status') is not None:
                stmt = stmt.where(Task.status == filters['status'])

            result = await session.execute(stmt)
            return result.scalar()
