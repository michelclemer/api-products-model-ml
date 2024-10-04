from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from src.api.deps import get_current_active_user
from src.crud.schemas.user.profile_schema import (ProfileUserCreate,
                                                  ProfileUserDetails,
                                                  ProfileUserUpdate)
from src.crud.schemas.user.user_schema import UserBase
from src.infra.auth.security import JWTBearer
from src.infra.container import Container
from src.services.user.user_services import ProfileService

router = APIRouter()


@router.post("/profile/create")
@inject
def create_profile(
        profile: ProfileUserCreate,
        profile_service: ProfileService = Depends(Provide[Container.profile_services])
):
    return profile_service.create_profile(profile)


@router.get("/profile/info/{usr_id}", response_model=ProfileUserDetails)
@inject
def get_profile_info(
    usr_id: Optional[str] = None,
    current_user: UserBase = Depends(get_current_active_user),
    profile_service: ProfileService = Depends(Provide[Container.profile_services])
):
    return profile_service.get_current_profile(int(usr_id) if usr_id else current_user.get('usr_id'))


@router.patch("/profile/update/{profile_id}", dependencies=[Depends(JWTBearer())])
@inject
def update_profile(
    profile: ProfileUserUpdate,
    profile_id: str,
    profile_service: ProfileService = Depends(Provide[Container.profile_services])
):
    return profile_service.update_profile(int(profile_id), profile)
