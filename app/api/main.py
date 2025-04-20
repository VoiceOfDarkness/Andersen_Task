from fastapi import APIRouter

from api.v1.routes import task

api_router = APIRouter()

api_router.include_router(task.task_router)
