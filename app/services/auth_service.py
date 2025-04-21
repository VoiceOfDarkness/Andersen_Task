from fastapi import HTTPException, status, Response, Request
from jose import JWTError

from models import User
from schemas.auth import LoginRequest
from services.base_service import BaseService
from schemas.user import UserCreate, UserInDB
from repository.user_repository import UserRepository
from core.security import hash_password, create_tokens, verify_password, decode_token


class AuthService(BaseService[User, UserInDB, UserCreate, UserRepository]):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def register(self, user: UserCreate, response: Response):
        if await self.user_repository.get_by_username(user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        db_user = UserInDB(
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
            password=hash_password(user.password),
        )

        user = await self.repository.create(db_user)
        access_token, refresh_token = create_tokens(user.id)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            samesite="lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=604800,
            samesite="strict"
        )

        return {"message": "Successfully registered", "user_id": user.id}

    async def login(self, sign_in_data: LoginRequest, response: Response):
        user = await self.user_repository.get_by_username(sign_in_data.username)
        if not user or not verify_password(sign_in_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

        access_token, refresh_token = create_tokens(user.id)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            samesite="lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=604800,
            samesite="strict"
        )
        return {"message": "Successfully logged in", "user_id": user.id}

    async def refresh(self, request: Request, response: Response):
        token = request.cookies.get("refresh_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

        try:
            payload = decode_token(token)
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            user = await self.repository.get(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

            new_access_token, new_refresh_token = create_tokens(user.id)
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                max_age=1800,
                samesite="lax"
            )

            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                max_age=604800,
                samesite="strict"
            )

            return {"message": "Tokens refreshed successfully"}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
