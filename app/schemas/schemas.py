from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime


class UserScheme(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_status: bool
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())

    class Config:
        orm_mode = True


class UserSchemeToken(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_status: bool

    class Config:
        orm_mode = True

class SignInRequest(BaseModel):
    user_email: EmailStr
    user_password: str = Field(..., min_length=4, max_length=20)

    class Config:
        orm_mode = True


class SignUpRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str = Field(..., min_length=4, max_length=20)
    user_password_repeat: str = Field(..., min_length=4, max_length=20)
    user_status: bool

    class Config:
        orm_mode = True


class UserUpdateRequest(BaseModel):
    user_name: str
    user_password: Optional[str]
    user_password_repeat: Optional[str]

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    users: List[UserScheme] = []

    class Config:
        orm_mode = True


class Results(BaseModel):
    result: Optional[UserListResponse]

    class Config:
        orm_mode = True


class ResultUserToken(BaseModel):
    result: Optional[UserSchemeToken]

    class Config:
        orm_mode = True


class ResultUser(BaseModel):
    result: Optional[UserScheme]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    result: Optional[Token]

