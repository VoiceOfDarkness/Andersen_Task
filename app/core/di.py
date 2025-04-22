from dependency_injector import containers, providers

from app.core.config import settings
from app.core.database import Database
from app.repository import TaskRepository, UserRepository
from app.services import AuthService, TaskService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.routes.task",
            "app.api.v1.routes.auth",
            "app.api.v1.routes.user",
            "app.api.deps"
        ]
    )

    database = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    user_repository = providers.Factory(UserRepository, session_factory=database.provided.session)
    task_repository = providers.Factory(TaskRepository, session_factory=database.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    task_service = providers.Factory(TaskService, task_repository=task_repository)
