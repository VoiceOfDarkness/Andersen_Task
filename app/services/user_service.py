from app.models import User
from app.services.base_service import BaseService
from app.schemas.user import UserCreate, UserInDB
from app.repository.user_repository import UserRepository


class UserService(BaseService[User, UserInDB, UserCreate, UserRepository]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
