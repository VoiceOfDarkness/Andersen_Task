from fastapi import HTTPException, status

from schemas.auth import LoginRequest
from schemas.user import UserCreate


def test_register(client, mock_auth_service, override_dependencies):
    user_data = {
        "username": "newuser",
        "password": "password123",
        "first_name": "New",
        "last_name": "User"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200

    assert "refresh_token" in response.cookies
    assert response.cookies["refresh_token"] == "mock_refresh_token"

    mock_auth_service.register.assert_called_once()


def test_login_success(client, mock_auth_service, override_dependencies):
    login_data = {
        "username": "testuser",
        "password": "password123"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 200

    assert "refresh_token" in response.cookies
    assert response.cookies["refresh_token"] == "mock_refresh_token"

    mock_auth_service.login.assert_called_once()


def test_login_failure(client, mock_auth_service, override_dependencies):
    mock_auth_service.login.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]

    mock_auth_service.login.assert_called_once()


def test_refresh_token_success(client, mock_auth_service, override_dependencies):
    client.cookies.set("refresh_token", "mock_refresh_token")

    response = client.post("/auth/refresh")

    assert response.status_code == 200

    assert "refresh_token" in response.cookies
    assert response.cookies["refresh_token"] == "new_mock_refresh_token"

    mock_auth_service.refresh.assert_called_once()


def test_refresh_token_missing(client, mock_auth_service, override_dependencies):
    mock_auth_service.refresh.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token missing"
    )

    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert "Refresh token missing" in response.json()["detail"]

    mock_auth_service.refresh.assert_called_once()


def test_refresh_token_invalid(client, mock_auth_service, override_dependencies):
    mock_auth_service.refresh.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )

    client.cookies.set("refresh_token", "invalid_refresh_token")

    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]

    mock_auth_service.refresh.assert_called_once()
