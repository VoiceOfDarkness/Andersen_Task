import uuid

from fastapi import HTTPException, status

from app.schemas.task import TaskStatus


def test_get_tasks(client, mock_task_service, override_dependencies):
    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 2
    assert data["total"] == 2

    mock_task_service.get_all.assert_called_once()


def test_get_tasks_with_filter(client, mock_task_service, override_dependencies):
    response = client.get("/api/v1/tasks?status=Completed")

    assert response.status_code == 200
    mock_task_service.get_all.assert_called_once()
    kwargs = mock_task_service.get_all.call_args[1]
    assert kwargs["status"] == TaskStatus.COMPLETED


def test_get_task_by_id(client, mock_task_service, override_dependencies):
    task_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"

    response = client.get(f"/api/v1/task?task_id={task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"
    assert data["status"] == "New"

    mock_task_service.get.assert_called_once_with(uuid.UUID(task_id))


def test_get_task_by_non_existent_id(client, mock_task_service, override_dependencies):
    mock_task_service.get.reset_mock()
    non_existent_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813cb"
    mock_task_service.get.side_effect = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                      detail=f"Task with id {non_existent_id} not found")

    response = client.get(f"/api/v1/task?task_id={non_existent_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    mock_task_service.get.assert_called_once_with(uuid.UUID(non_existent_id))
