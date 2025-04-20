from repository.base_repository import BaseRepository
from models.task import Task
from schemas.task import TaskInDB


class TaskRepository(BaseRepository[Task, TaskInDB, TaskInDB]):
    def __init__(self, session_factory):
        super().__init__(session_factory, Task)
