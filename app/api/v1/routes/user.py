import uuid

from typing import Optional

from fastapi import APIRouter, Depends, Query, Body

from dependency_injector.wiring import inject, Provide

from core.di import Container
from services.task_service import TaskService
from api.deps import CurrentUser
from schemas.pagination import PaginationResponse, PaginationParams
from schemas.task import TaskCreate, TaskInDB, TaskUpdate, TaskUpdateInDB, TaskResponse, TaskStatus

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.post("/task")
@inject
async def create_task(task: TaskCreate,
                      current_user: CurrentUser,
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    task_entity = TaskInDB(user_id=current_user.id, **task.model_dump())
    return await task_service.create(task_entity)


@user_router.delete("/task", responses={204: {"detail": "deleted successfully"}})
@inject
async def delete_task(current_user: CurrentUser,
                      task_id: uuid.UUID = Query(..., example="fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.delete_user_task(task_id, current_user.id)


@user_router.patch("/task")
@inject
async def update_task(current_user: CurrentUser,
                      task: Optional[TaskUpdate] = Body(None),
                      status: Optional[TaskStatus] = Query(None),
                      task_id: uuid.UUID = Query(..., example="fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.update_user_task(task_id, current_user.id,
                                               TaskUpdateInDB(status=status, **task.model_dump()))


@user_router.get("/task", response_model=PaginationResponse[TaskResponse])
@inject
async def get_task(current_user: CurrentUser,
                   pagination: PaginationParams = Depends(),
                   status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
                   task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.get_user_task(current_user.id, status=status, pagination=pagination)
