from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.crud.schemas.user.user_schema import UserResponse


class SignIn(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    email: EmailStr
    password: str
    name: str


class Payload(BaseModel):
    id: int
    email: str
    name: str
    is_superuser: bool


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: UserResponse
