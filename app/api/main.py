from fastapi import APIRouter

from app.api.v1.routes import auth, task, user

api_router = APIRouter()

api_router.include_router(auth.auth_router)
api_router.include_router(user.user_router)
api_router.include_router(task.task_router)
