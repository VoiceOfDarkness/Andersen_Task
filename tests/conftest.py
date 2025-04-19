import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.config import settings
from app.core.database import Database


@pytest.fixture(autouse=True)
def db():
    return Database(db_url=settings.TEST_DATABASE_URL)


@pytest.fixture(autouse=True)
def mock_db_session():
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()

    mock_session_factory = MagicMock(return_value=mock_session)
    mock_session_factory.remove = AsyncMock()

    return mock_session, mock_session_factory
