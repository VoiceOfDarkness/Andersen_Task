from contextlib import asynccontextmanager
from app.core.di import Container
from fastapi import FastAPI
from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.container = Container()
    db = app.container.database()
    await db.init_db()

    yield


app = FastAPI(lifespan=lifespan)
app.container = Container()
app.include_router(api_router)
