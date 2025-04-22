from sqlalchemy.future import select

from app.repository.base_repository import BaseRepository
from app.models.user import User
from app.schemas.user import UserInDB


class UserRepository(BaseRepository[User, UserInDB, UserInDB]):
    def __init__(self, session_factory):
        super().__init__(session_factory, User)

    async def get_by_username(self, username: str) -> User:
        async with self.session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.username == username)
            record = await session.execute(stmt)

            return record.scalars().one_or_none()
