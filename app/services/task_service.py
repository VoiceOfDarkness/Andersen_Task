from models import Task
from repository.task_repository import TaskRepository
from schemas.task import TaskInDB, TaskUpdateInDB, TaskStatus
from services.base_service import BaseService


class TaskService(BaseService[Task, TaskInDB, TaskUpdateInDB, TaskRepository]):
    def __init__(self, task_repository: TaskRepository):
        super().__init__(task_repository)