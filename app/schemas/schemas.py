from pydantic import BaseModel, Field, EmailStr,  constr
from datetime import datetime


class UserScheme(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_status: bool
    created_at: datetime = Field(default_factory=datetime.now())#.strftime("%Y-%m-%d %H:%M:%S")
    updated_at: datetime = Field(default_factory=datetime.now())#.strftime("%Y-%m-%d %H:%M:%S")


class SignInRequest(BaseModel):
    user_email: EmailStr
    user_password: str


class SignUpRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str
    user_rep_password: str
    user_status: bool


class InsertDB(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str
    user_status: bool


class UserUpdateRequest(BaseModel):
    user_name: str
    user_status: bool
    user_password: str
    user_rep_password: str


class UserListResponse(BaseModel):
    users: list[UserScheme]
