from fastapi import HTTPException, status
from uuid import UUID

from starlette.responses import JSONResponse

from core.exceptions import ObjectNotFoundException
from models.base import Base
from pydantic import BaseModel
from repository.base_repository import BaseRepository


class BaseService[Model: Base, CreateSchema: BaseModel, UpdateSchema: BaseModel, RepoType: BaseRepository]:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, data: CreateSchema):
        try:
            await self.repository.create(data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Can't create an object: {str(e)}"
            )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="created")

    async def update(self, id: UUID, data: UpdateSchema):
        try:
            return await self.repository.update(id, data)
        except ObjectNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {id} not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Can't update an object: {str(e)}"
            )

    async def delete(self, id: UUID):
        try:
            return await self.repository.delete(id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Can't delete an object: {str(e)}"
            )

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
            return await self.repository.get_all(**filters)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Can't get an object: {str(e)}"
            )
