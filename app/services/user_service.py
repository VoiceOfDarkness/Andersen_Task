from models import User
from services.base_service import BaseService
from schemas.user import UserCreate, UserInDB
from repository.user_repository import UserRepository


class UserService(BaseService[User, UserInDB, UserCreate, UserRepository]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
