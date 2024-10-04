from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.deps import can_create_user, get_current_active_user
from src.crud.schemas.user.auth_schema import SignIn, SignInResponse, SignUp
from src.crud.schemas.user.user_schema import UserBase, UserResponse
from src.infra.container import Container
from src.services.user.auth_service import AuthService

router = APIRouter()


@router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(user_info: SignIn, service: AuthService = Depends(Provide[Container.auth_services])):
    return service.sign_in(user_info)


@router.post("/sign-up", response_model=UserResponse)
@inject
async def sign_up(user_info: SignUp, service: AuthService = Depends(Provide[Container.auth_services])):
    return service.sign_up(user_info)


@router.get("/me", response_model=UserBase)
@inject
async def get_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user
