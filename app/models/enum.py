from enum import Enum


class TaskStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
