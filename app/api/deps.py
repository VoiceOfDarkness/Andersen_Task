from fastapi import Depends, Request, status, HTTPException

from dependency_injector.wiring import inject, Provide
from jose import JWTError

from core.security import decode_token
from core.di import Container
from services import AuthService


@inject
async def get_current_user(request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await auth_service.get(user_id)
    if not user:
        raise credentials_exception
    return user
