from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
import uuid

from fastapi.params import Query

from core.di import Container
from schemas.task import TaskResponse, TaskCreate, TaskInDB, TaskUpdate, TaskUpdateInDB, TaskStatus
from typing import List, Optional

from services.task_service import TaskService

task_router = APIRouter(tags=["task"])


@task_router.get("/tasks", response_model=List[TaskResponse])
@inject
async def get_tasks(
        status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
        task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.get_all(status=status)


@task_router.get("/task", response_model=Optional[TaskResponse])
@inject
async def task(status: Optional[TaskStatus] = Query(None, description="Filter tasks by status"),
               task_id: uuid.UUID = Query(..., example="fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"),
               task_service: TaskService = Depends(Provide[Container.task_service])):
    print(status)
    return await task_service.get(task_id, status=status)


@task_router.post("/task")
@inject
async def create_task(task: TaskCreate,
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    task_entity = TaskInDB(user_id=uuid.UUID("a9ae4da5-fedf-4a3f-b7bb-6e47c4396c6e"), **task.model_dump())
    return await task_service.create(task_entity)


@task_router.delete("/task")
@inject
async def delete_task(task_id: uuid.UUID = Query(..., example="fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.delete(task_id)


@task_router.patch("/task")
@inject
async def update_task(task: TaskUpdate,
                      task_id: uuid.UUID = Query(..., example="fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"),
                      task_service: TaskService = Depends(Provide[Container.task_service])):
    return await task_service.update(task_id, TaskUpdateInDB(**task.model_dump()))
