from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
import uuid

from fastapi.params import Query

from app.core.di import Container
from app.models import User
from app.schemas.pagination import PaginationParams
from app.schemas.task import TaskResponse, TaskStatus
from app.schemas.pagination import PaginationResponse
from typing import Optional

from app.api.deps import get_current_user
from app.services.task_service import TaskService

task_router = APIRouter(tags=["task"])


@task_router.get("/tasks", response_model=PaginationResponse[TaskResponse])
@inject
async def get_tasks(
        _current_user: User = Depends(get_current_user),
        pagination: PaginationParams = Depends(),
        status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
        task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.get_all(status=status, pagination=pagination)


@task_router.get("/task", response_model=Optional[TaskResponse])
@inject
async def get_task(_current_user: User = Depends(get_current_user),
                   task_id: uuid.UUID = Query(..., examples=["fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"]),
                   task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.get(task_id)
