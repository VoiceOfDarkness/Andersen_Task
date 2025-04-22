from uuid import UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.exceptions import ObjectNotFoundException
from app.models.base import Base
from app.repository.base_repository import BaseRepository


class BaseService[Model: Base, CreateSchema: BaseModel, UpdateSchema: BaseModel, RepoType: BaseRepository]:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, data: CreateSchema):
        try:
            await self.repository.create(data)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="created")

    async def update(self, id: UUID, data: UpdateSchema):
        try:
            return await self.repository.update(id, data)
        except ObjectNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {id} not found"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    async def delete(self, id: UUID):
        try:
            await self.repository.delete(id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="deleted")

    async def get(self, id: UUID):
        try:
            return await self.repository.get(id)
        except ObjectNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {id} not found"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    async def get_all(self):
        try:
            return await self.repository.get_all()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )
