from uuid import UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from core.exceptions import ObjectNotFoundException
from models import Task
from repository.task_repository import TaskRepository
from schemas.pagination import PaginationResponse
from schemas.task import TaskInDB, TaskUpdateInDB
from services.base_service import BaseService


class TaskService(BaseService[Task, TaskInDB, TaskUpdateInDB, TaskRepository]):
    def __init__(self, task_repository: TaskRepository):
        super().__init__(task_repository)
        self.task_repository = task_repository

    async def get(self, id: UUID):
        try:
            return await self.task_repository.get(id)
        except ObjectNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {id} not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error"
            )

    async def get_all(self, **filters):
        try:
            pagination = filters.pop("pagination", None)

            items = await self.task_repository.get_all(pagination, **filters)

            total_items = await self.task_repository.count(**filters)

            total_pages = (total_items + pagination.page_size - 1) // pagination.page_size

            return PaginationResponse(
                items=items,
                total=total_items,
                page=pagination.page,
                page_size=pagination.page_size,
                pages=total_pages
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error"
            )

    async def delete_user_task(self, id: UUID, user_id: UUID):
        try:
            await self.task_repository.delete_user_task(id, user_id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error"
            )
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="deleted")

    async def update_user_task(self, id: UUID, user_id: UUID, task: TaskUpdateInDB):
        try:
            return await self.task_repository.update_user_task(id, user_id, task)
        except ObjectNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {id} not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error"
            )

    async def get_user_task(self, user_id: UUID, **filters):
        try:
            pagination = filters.pop("pagination", None)

            items = await self.task_repository.get_user_task(user_id, pagination, **filters)

            total_items = await self.task_repository.count(**filters)

            total_pages = (total_items + pagination.page_size - 1) // pagination.page_size

            return PaginationResponse(
                items=items,
                total=total_items,
                page=pagination.page,
                page_size=pagination.page_size,
                pages=total_pages
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error"
            )
