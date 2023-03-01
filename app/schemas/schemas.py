from typing import List

from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class User(BaseModel):
    user_id: int
    created_at: datetime
    user_name: str
    user_email: EmailStr
    user_status: bool

    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    user_email: EmailStr
    user_password: constr(min_lenght=7, max_length=100)


class SignUpRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: constr(min_lenght=7, max_length=100)
    user_rep_password: constr(min_lenght=7, max_length=100)


class UserUpdateRequest(BaseModel):
    user_name: str
    user_status: bool
    user_password: constr(min_lenght=7, max_length=100)
    user_rep_password: constr(min_lenght=7, max_length=100)


class UserListResponse(BaseModel):
    Users: List[User]
