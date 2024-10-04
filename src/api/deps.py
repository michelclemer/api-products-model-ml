from typing import Any, Dict

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from src.crud.models.user import User
from src.crud.schemas.user.auth_schema import Payload
from src.infra.auth.security import ALGORITHM, JWTBearer
from src.infra.commons.exceptions import AuthError
from src.infra.container import Container
from src.infra.settings import settings as configs
from src.services.user.user_services import UserService


@inject
def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_services]),
) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = service.get_by_id(token_data.id)
    user_dict = current_user.dict()
    user_dict["roles"] = [role.role.rol_name for role in current_user.roles]
    if not current_user:
        raise AuthError(detail="User not found")
    return user_dict


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if isinstance(current_user, dict):
        if not current_user.get("is_active"):
            raise AuthError("Inactive user")
    else:
        if not current_user.is_active:
            raise AuthError("Inactive user")

    return current_user


def can_create_user(current_user: User = Depends(get_current_user)):
    roles = ['Gerente', 'Gerente Comercial', 'Surpervisor Comercial', 'Gerencia Logistica', 'Supervisor Logistica']
    if isinstance(current_user, dict):
        if not current_user.get("is_superuser"):
            raise AuthError("It's not a super user")
    else:
        if not current_user.is_superuser or current_user['roles'] not in roles:
            raise AuthError("Has no permission to create user")
    return current_user


def get_current_user_with_no_exception(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_services]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        return None
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user