from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserInDB
from app.services.base_service import BaseService


class UserService(BaseService[User, UserInDB, UserCreate, UserRepository]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
