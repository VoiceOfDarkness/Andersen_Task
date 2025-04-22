from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.di import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = app.container.database()
    await db.init_db()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.container = Container()
app.include_router(api_router, prefix=settings.API_V1_STR)
