from typing import Optional

from fastapi import HTTPException

from sqlalchemy.sql import select, insert, update, delete

from models.models import User
from schemas.schemas import UserScheme, UserListResponse, UserUpdateRequest, SignUpRequest, InsertDB
from databases import Database

from utils.security import hash


class UserServices:
    def __init__(self, db: Database):
        self.db = db

    async def get_users(self) -> UserListResponse:
        user_list = await self.db.fetch_all(query=select(User))
        return UserListResponse(users=[UserScheme(**item) for item in user_list])

    async def get_user(self, user_id: int) -> Optional[UserScheme]:
        query = select(User).where(User.user_id == user_id)
        user = await self.db.fetch_one(query=query)
        if not user:
            raise HTTPException(status_code=404, detail='User does not exist')
        return UserScheme(**dict(user))

    async def create_user(self, user: SignUpRequest) -> UserScheme:
        new_user = dict(user)
        if not (new_user["user_password"] == new_user["user_rep_password"]):
            raise HTTPException(status_code=404, detail='Passwords do not match')
        new_user.pop("user_rep_password", None)
        hashed_password = hash.encrypt_password(password=new_user["user_password"])
        new_user["user_password"] = hashed_password
        query = insert(User).values(new_user)
        user_id = await self.db.execute(query=query)
        new_user_db = await self.get_user(user_id)
        return new_user_db

    async def delete_user(self, user_id: int):
        query = delete(User).where(User.user_id == user_id)
        await self.db.execute(query=query)

    async def check_for_existing(self, user_id: int):
        query = select(User).where(User.user_id == user_id)
        user = await self.db.fetch_one(query=query)
        if not user:
            raise HTTPException(status_code=404, detail='User does not exist')

    async def update_user(self, user_id: int, user: UserUpdateRequest) -> UserScheme:
        await self.check_for_existing(user_id=user_id)
        update_data = dict(user)
        if not (update_data["user_password"] == update_data["user_rep_password"]):
            raise HTTPException(status_code=404, detail='Passwords do not match')
        hashed_password = hash.encrypt_password(password=update_data["user_password"])
        update_data["user_password"] = hashed_password
        update_data.pop("user_rep_password", None)
        query = update(User).where(User.user_id == user_id).values(update_data)
        await self.db.execute(query=query)
        updated_user = await self.get_user(user_id=user_id)
        return updated_user


