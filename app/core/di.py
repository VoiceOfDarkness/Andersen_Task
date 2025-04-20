from dependency_injector import containers, providers

from .config import settings
from .database import Database

from repository import UserRepository
from services import UserService


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    user_repository = providers.Factory(UserRepository, session_factory=database.provided.session)
    task_repository = providers.Factory(UserRepository, session_factory=database.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    task_service = providers.Factory(UserService, user_repository=user_repository)
