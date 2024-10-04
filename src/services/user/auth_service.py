from datetime import timedelta
from typing import List

from src.crud.models.user import User
from src.crud.repository.user_repository import UserRepository
from src.crud.schemas.user.auth_schema import Payload, SignIn, SignUp
from src.crud.schemas.user.user_schema import FindUser
from src.infra.auth.security import (create_access_token, get_password_hash,
                                     verify_password)
from src.infra.commons.exceptions import AlreadyExistsError, AuthError
from src.infra.settings import settings as configs
from src.services.user.user_services import BaseService
from src.utils.hash import get_rand_hash


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository, ):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn):
        find_user = FindUser()
        find_user.email = sign_in_info.email
        user: User | None = self.user_repository.get_by_email(sign_in_info.email)
        if not user:
            raise AuthError(detail="Incorrect email or password")
        found_user: dict = self.user_repository.read_by_id(user.id)
        if not found_user.get("is_active"):
            raise AuthError(detail="Account is not active")
        if not verify_password(sign_in_info.password, user.password):
            raise AuthError(detail="Incorrect email or password")

        payload = Payload(
            id=found_user.get("id"),
            email=found_user.get("email"),
            name=found_user.get("name"),
            is_superuser=found_user.get("is_superuser"),
        )
        token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.dict(), token_lifespan)
        sign_in_result = {
            "access_token": access_token,
            "expiration": expiration_datetime,
            "user_info": found_user,
        }
        return sign_in_result

    def sign_up(self, user_info: SignUp):
        user_token = get_rand_hash()
        user = User(**user_info.dict(exclude_none=True), is_active=True, is_superuser=False, user_token=user_token)
        user.password = get_password_hash(user_info.password)
        try:
            created_user = self.user_repository.create(user)
        except Exception:
            raise AlreadyExistsError(detail="User already exists")
        delattr(created_user, "password")
        return created_user
