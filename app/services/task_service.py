from uuid import UUID

from fastapi import HTTPException, status

from core.exceptions import ObjectNotFoundException
from models import Task
from repository.task_repository import TaskRepository
from schemas.pagination import PaginationResponse
from schemas.task import TaskInDB, TaskUpdateInDB
from services.base_service import BaseService


class TaskService(BaseService[Task, TaskInDB, TaskUpdateInDB, TaskRepository]):
    def __init__(self, task_repository: TaskRepository):
        super().__init__(task_repository)

    async def get(self, id: UUID, **filters):
        try:
            return await self.repository.get(id, **filters)
        except ObjectNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {id} not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Can't get an object: {str(e)}"
            )

    async def get_all(self, **filters):
        try:
            pagination = filters.pop("pagination", None)

            items = await self.repository.get_all(pagination, **filters)

            total_items = await self.repository.count(**filters)

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
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Can't get an object: {str(e)}"
            )
