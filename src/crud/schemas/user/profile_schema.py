from typing import Optional

from pydantic import BaseModel

from src.crud.schemas.base_schema import FindBase
from src.crud.schemas.user.user_schema import UserBase
from src.utils.schema import partial_model


class ProfileUserBase(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    cpf: Optional[str] = None
    avatar: Optional[dict] = None


class ProfileUserDetails(ProfileUserBase):
    user: Optional[UserBase] = None


class ProfileUserCreate(ProfileUserBase):
    pass


class ProfileUserUpdate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    cpf: Optional[str] = None
    avatar: Optional[dict] = None


@partial_model
class FindProfileUser(ProfileUserBase, FindBase):
    pass
