from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Database


class TestModel(Base):
    __test__ = False
    __tablename__ = 'test_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


@pytest.mark.asyncio
async def test_database_initialization(db):
    assert db._engine is not None
    assert db._session_factory is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_init_db():
    mock_conn = AsyncMock()
    cm = AsyncMock()
    cm.__aenter__.return_value = mock_conn

    mock_engine = MagicMock()
    mock_engine.begin.return_value = cm

    with patch('builtins.__import__', return_value=MagicMock()), \
            patch('app.core.database.Base.metadata.create_all') as mock_create_all:
        db = Database("postgresql+asyncpg://postgres:postgres@localhost:5432/test_db")
        db._engine = mock_engine

        await db.init_db()

        mock_conn.run_sync.assert_called_once()
        run_sync_func = mock_conn.run_sync.call_args[0][0]

        mock_sync_conn = MagicMock()
        run_sync_func(mock_sync_conn)

        mock_create_all.assert_called_once()


@pytest.mark.asyncio(loop_scope="session")
async def test_session_commit_success(db, mock_db_session):
    mock_session, mock_session_factory = mock_db_session
    db._session_factory = mock_session_factory

    async with db.session() as session:
        assert session == mock_session

    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()
    mock_session_factory.remove.assert_called_once()


@pytest.mark.asyncio(loop_scope="session")
async def test_session_rollback_on_error(db, mock_db_session):
    mock_session, mock_session_factory = mock_db_session
    mock_session.commit = AsyncMock(side_effect=SQLAlchemyError("Test Error"))
    db._session_factory = mock_session_factory

    with patch('logging.error') as mock_log_error:
        with pytest.raises(SQLAlchemyError, match="Test Error"):
            async with db.session():
                raise SQLAlchemyError("Test Error")

        mock_session.commit.assert_not_called()
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
        mock_session_factory.remove.assert_called_once()

        assert mock_log_error.call_count == 2


@pytest.mark.asyncio(loop_scope="session")
async def test_session_cleanup_on_exception(db, mock_db_session):
    mock_session, mock_session_factory = mock_db_session
    db._session_factory = mock_session_factory

    try:
        async with db.session() as session:
            assert session == mock_session
            raise ValueError("Test exception")
    except ValueError:
        pass

    mock_session.commit.assert_not_called()
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
    mock_session_factory.remove.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-xvs"])
