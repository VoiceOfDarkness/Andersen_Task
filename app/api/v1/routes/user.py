import uuid

from typing import Optional, Dict

from fastapi import APIRouter, Depends, Query, Body

from dependency_injector.wiring import inject, Provide

from api.deps import get_current_user
from core.di import Container
from models import User
from services.task_service import TaskService
from schemas.pagination import PaginationResponse, PaginationParams
from schemas.task import TaskCreate, TaskInDB, TaskUpdate, TaskUpdateInDB, TaskResponse, TaskStatus

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.post("/task")
@inject
async def create_task(task: TaskCreate,
                      current_user: User = Depends(get_current_user),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    task_entity = TaskInDB(user_id=current_user.id, **task.model_dump())
    return await task_service.create(task_entity)


@user_router.delete("/task", responses={204: {"detail": "deleted successfully"}})
@inject
async def delete_task(current_user: User = Depends(get_current_user),
                      task_id: uuid.UUID = Query(..., examples=["fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"]),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.delete_user_task(task_id, current_user.id)


@user_router.patch("/task")
@inject
async def update_task(current_user: User = Depends(get_current_user),
                      task: Optional[TaskUpdate] = Body(None),
                      status: Optional[TaskStatus] = Query(None),
                      task_id: uuid.UUID = Query(..., examples=["fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"]),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    task_data: TaskUpdate | Dict = task.model_dump() if task else {}
    return await task_service.update_user_task(task_id, current_user.id,
                                               TaskUpdateInDB(status=status, **task_data))


@user_router.get("/tasks", response_model=PaginationResponse[TaskResponse])
@inject
async def get_tasks(current_user: User = Depends(get_current_user),
                    pagination: PaginationParams = Depends(),
                    status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
                    task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.get_user_task(current_user.id, status=status, pagination=pagination)
