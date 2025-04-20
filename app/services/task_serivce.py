from models import Task
from repository.task_repository import TaskRepository
from schemas.task import TaskInDB
from services.base_service import BaseService


class TaskService(BaseService[Task, TaskInDB, TaskInDB, TaskRepository]):
    def __init__(self, repository: TaskRepository):
        super().__init__(repository)
