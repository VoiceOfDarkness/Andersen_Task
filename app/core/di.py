from dependency_injector import containers, providers

from .config import settings
from .database import Database

from repository import UserRepository, TaskRepository
from services import UserService, TaskService, AuthService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.routes.task",
            "api.v1.routes.auth",
            "api.v1.routes.user",
            "api.deps"
        ]
    )

    database = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    user_repository = providers.Factory(UserRepository, session_factory=database.provided.session)
    task_repository = providers.Factory(TaskRepository, session_factory=database.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    task_service = providers.Factory(TaskService, task_repository=task_repository)
