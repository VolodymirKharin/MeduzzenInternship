from fastapi import HTTPException

from sqlalchemy.sql import select, insert, update, delete
from models.models import User
from schemas.schemas import UserScheme, UserListResponse, UserUpdateRequest, SignUpRequest, Results, ResultUser
from databases import Database


from utils.security import hash
from datetime import datetime


class UserServices:
    def __init__(self, db: Database):
        self.db = db

    async def get_users(self) -> Results:
        user_list = await self.db.fetch_all(query=select(User))
        result = UserListResponse(users=[UserScheme(**item) for item in user_list])
        return Results(result=result)

    async def get_user(self, user_id: int) -> ResultUser:
        query = select(User).where(User.user_id == user_id)
        user = await self.db.fetch_one(query=query)
        if not user:
            raise HTTPException(status_code=404, detail='User does not exist')
        return ResultUser(result=UserScheme(**dict(user)))

    async def create_user(self, user: SignUpRequest) -> ResultUser:
        if not (user.user_password == user.user_password_repeat):
            raise HTTPException(status_code=422, detail='Passwords do not match')
        await self.check_email(user_email=user.user_email)
        new_user = {
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_password": hash.encrypt_password(password=user.user_password),
            "user_status": user.user_status,

        }
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

    async def get_user_by_email(self, user_email: str) -> UserScheme:
        query = select(User).where(User.user_email == user_email)
        user = await self.db.fetch_one(query=query)
        if not user:
            return None
        return ResultUser(result=UserScheme(**dict(user)))

    async def check_email(self, user_email: str) -> ResultUser:
        query = select(User).where(User.user_email == user_email)
        user = await self.db.fetch_one(query=query)
        if user:
            raise HTTPException(status_code=400, detail='email exist')

    async def get_user_password(self, user_email: str) -> str:
        query = select(User).where(User.user_email == user_email)
        user = await self.db.fetch_one(query=query)
        return user.user_password

    async def update_user(self, user_id: int, user: UserUpdateRequest) -> ResultUser:
        await self.check_for_existing(user_id=user_id)
        if user.user_password is not None:
            if not (user.user_password == user.user_password_repeat):
                raise HTTPException(status_code=404, detail='Passwords do not match')
            update_data = {
                "user_name": user.user_name,
                "user_password": hash.encrypt_password(password=user.user_password),
            }
        else:
            update_data = {
                "user_name": user.user_name,
            }
        query = update(User).where(User.user_id == user_id).values(update_data)
        await self.db.execute(query=query)
        updated_user = await self.get_user(user_id=user_id)
        return updated_user
