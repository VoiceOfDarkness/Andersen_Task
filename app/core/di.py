from dependency_injector import containers, providers

from .config import settings
from .database import Database


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, db_url=settings.DATABASE_URL)
