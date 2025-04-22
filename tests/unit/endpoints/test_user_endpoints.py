import uuid

from fastapi import HTTPException, status
from models.task import TaskStatus


def test_create_task(client, mock_task_service, override_dependencies):
    task_data = {
        "title": "New Task",
        "description": "New Task Description",
        "status": "New"
    }

    response = client.post("/user/task", json=task_data)

    print(response.status_code)

    assert response.status_code == 201
    assert response.json()["title"] == "New Task"
    assert response.json()["description"] == "New Task Description"

    mock_task_service.create.assert_called_once()

    task_arg = mock_task_service.create.call_args[0][0]
    assert task_arg.title == "New Task"
    assert task_arg.description == "New Task Description"
    assert task_arg.user_id == uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")


def test_get_user_tasks(client, mock_task_service, override_dependencies):
    response = client.get("/user/tasks")

    assert response.status_code == 200
    assert "items" in response.json()
    assert len(response.json()["items"]) == 1
    assert response.json()["total"] == 1

    mock_task_service.get_user_task.assert_called_once()
    user_id_arg = mock_task_service.get_user_task.call_args[0][0]
    assert user_id_arg == uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")


def test_get_tasks_with_filter(client, mock_task_service, override_dependencies):
    response = client.get("/user/tasks?status=New")

    assert response.status_code == 200

    kwargs = mock_task_service.get_user_task.call_args[1]
    assert kwargs["status"] == TaskStatus.NEW


def test_update_task(client, mock_task_service, override_dependencies):
    task_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated Task Description"
    }

    response = client.patch(f"/user/task?task_id={task_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task Title"
    assert response.json()["description"] == "Updated Task Description"

    mock_task_service.update_user_task.assert_called_once()
    call_args = mock_task_service.update_user_task.call_args
    assert call_args[0][0] == uuid.UUID(task_id)
    assert call_args[0][1] == uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")

    update_obj = call_args[0][2]
    assert update_obj.title == "Updated Task Title"
    assert update_obj.description == "Updated Task Description"


def test_update_task_status(client, mock_task_service, override_dependencies):
    task_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"

    response = client.patch(f"/user/task?task_id={task_id}&status=Completed", json={})

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"

    mock_task_service.update_user_task.assert_called_once()
    call_args = mock_task_service.update_user_task.call_args
    update_obj = call_args[0][2]
    assert update_obj.status == TaskStatus.COMPLETED


def test_update_nonexistent_task(client, mock_task_service, override_dependencies):
    task_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813cb"
    update_data = {"title": "Updated Title"}

    mock_task_service.update_user_task.side_effect = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                                   detail=f"object with id {id} not found")

    response = client.patch(f"/user/task?task_id={task_id}", json=update_data)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_task(client, mock_task_service, override_dependencies):
    task_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca"

    response = client.delete(f"/user/task?task_id={task_id}")

    assert response.status_code == 204

    mock_task_service.delete_user_task.assert_called_once_with(
        uuid.UUID(task_id),
        uuid.UUID("fa90ea32-1d7c-4ee8-9b68-07e6b4a813ca")
    )


def test_delete_nonexistent_task(client, mock_task_service, override_dependencies):
    task_id = "fa90ea32-1d7c-4ee8-9b68-07e6b4a813cb"

    mock_task_service.delete_user_task.side_effect = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                                   detail=f"object with id {id} not found")

    response = client.delete(f"/user/task?task_id={task_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
