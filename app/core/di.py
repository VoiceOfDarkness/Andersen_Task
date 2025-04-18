from dependency_injector import containers, providers
from database import Database
from config import settings


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, db_url=settings.async_database_url)
