import asyncio
import logging
import traceback
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url)
        self._session_factory = async_scoped_session(async_sessionmaker(bind=self._engine, class_=AsyncSession),
                                                     scopefunc=asyncio.current_task)

    async def init_db(self):
        import models

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            logging.error(f"Session rollback due to exception: {e}")
            logging.error(traceback.format_exc())
            await session.rollback()
        finally:
            await session.close()
            await self._session_factory.remove()
