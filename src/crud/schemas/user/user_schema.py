from typing import Dict, Optional

from pydantic import BaseModel, EmailStr, Field

from src.crud.schemas.base_schema import FindBase
from src.utils.schema import partial_model


class RoleListParams(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    unit: Optional[int] = None
    phone: Optional[str] = None
    permissions: Optional[Dict[str, dict]] = Field(
        default=None,
        examples=[{
            "manager-routes": {
                "create-route": True,
                "edit-route": True,
                "start-route": False,
                "approve-route": False,
                "finish-route": False
            },
            "manager-users": {
                "edit-user": False,
                "delete-user": True
            },
        }]
    )


class UserCreate(UserBase):
    role_id: int
    password: Optional[str] = ""


class UserResponse(UserBase):
    role: dict
    profile: Optional[dict]
    id: int


class UserUpdate(UserBase):
    password: Optional[str] = None


@partial_model
class FindUser(UserBase, FindBase):
    email__eq: Optional[str]


class UserList(BaseModel):
    data: list[UserResponse]
    total: int
    page: int
    limit: int


class UnitResponse(BaseModel):
    id: int
    unit_name: str
