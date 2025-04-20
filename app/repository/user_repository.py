from repository.base_repository import BaseRepository
from models.user import User
from schemas.user import UserInDB


class UserRepository(BaseRepository[User, UserInDB, UserInDB]):
    def __init__(self, session_factory):
        super().__init__(session_factory, User)
