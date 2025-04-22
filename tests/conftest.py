import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from api.deps import get_current_user
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from schemas.pagination import PaginationResponse
from services import TaskService

from app.core.config import settings
from app.core.database import Database
from app.main import app
from app.schemas.task import TaskStatus


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def db():
    return Database(db_url=settings.TEST_DATABASE_URL)


@pytest.fixture
def mock_db_session():
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()

    mock_session_factory = MagicMock(return_value=mock_session)
    mock_session_factory.remove = AsyncMock()

    return mock_session, mock_session_factory


@pytest.fixture
def mock_current_user():
    user = MagicMock()
    user.id = uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")
    user.username = "testuser"
    user.first_name = "Test"
    user.last_name = "Test"
    user.password = "Test"
    return user


@pytest.fixture
def mock_task_service():
    service = AsyncMock(spec=TaskService)

    task_id = uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")
    user_id = uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")

    async def mock_create(task):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "id": str(task_id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": str(user_id),
        })

    service.create.side_effect = mock_create

    async def mock_get_user_task(user_id, **filters):
        items = [
            {
                "id": task_id,
                "title": "Test Task",
                "description": "Test Description",
                "status": TaskStatus.NEW,
                "user_id": user_id,
                "user": {
                    "first_name": "string",
                    "last_name": "Test",
                    "username": "Test"
                }
            }
        ]
        return PaginationResponse(
            items=items,
            total=1,
            page=filters.get("pagination").page if "pagination" in filters else 1,
            page_size=filters.get("pagination").page_size if "pagination" in filters else 10,
            pages=1
        )

    service.get_user_task.side_effect = mock_get_user_task

    async def mock_update_user_task(task_id, user_id, task):
        if task_id == uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"):
            return {
                "id": task_id,
                "title": task.title if task.title is not None else "Test Task",
                "description": task.description if task.description is not None else "Test Description",
                "status": task.status if task.status is not None else TaskStatus.NEW,
                "user_id": user_id,
                "user": {
                    "id": user_id,
                    "username": "testuser",
                    "first_name": "Test",
                    "last_name": "Test"
                }
            }
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {task_id} not found")

    service.update_user_task.side_effect = mock_update_user_task

    async def mock_delete_user_task(task_id, user_id):
        expected_task_id = uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")
        expected_user_id = uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")

        if task_id != expected_task_id or user_id != expected_user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with id {task_id} not found")
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    service.delete_user_task.side_effect = mock_delete_user_task

    return service


@pytest.fixture
def override_dependencies(mock_current_user, mock_task_service):
    async def mock_get_current_user():
        return mock_current_user

    app.dependency_overrides = {
        get_current_user: mock_get_current_user,
    }
    app.container.task_service.override(mock_task_service)

    yield

    app.dependency_overrides.clear()
