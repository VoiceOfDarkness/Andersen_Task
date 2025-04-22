from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Response

from app.core.di import Container
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate
from app.services import AuthService

auth_router = APIRouter(tags=["auth"], prefix="/auth")


@auth_router.post("/register")
@inject
async def register(user_data: UserCreate,
                   response: Response,
                   auth_service: AuthService = Depends(Provide[Container.auth_service])):
    return await auth_service.register(user_data, response)


@auth_router.post("/login")
@inject
async def login(sign_in_data: LoginRequest,
                response: Response,
                auth_service: AuthService = Depends(Provide[Container.auth_service])):
    return await auth_service.login(sign_in_data, response)


@auth_router.post("/refresh")
@inject
async def refresh(request: Request,
                  response: Response,
                  auth_service: AuthService = Depends(Provide[Container.auth_service])):
    return await auth_service.refresh(request, response)
