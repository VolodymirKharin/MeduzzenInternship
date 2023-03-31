from sqlalchemy.sql import select, delete, update
from databases import Database
from fastapi import HTTPException
from starlette import status
from models.models import member
from schemas.action_schemas import Member, AllMembers, MemberListResponse
from schemas.user_schemas import UserScheme

from schemas.admin_schemas import AdminsList


class AdminServices:
    def __init__(self, db: Database, current_user: UserScheme = None):
        self.db = db
        self.current_user_id = None if not current_user else current_user.user_id

    async def get_company_members(self) -> AllMembers:

        member_list = await self.db.fetch_all(query=select(member))
        result = MemberListResponse(users=[Member(**item) for item in member_list])
        return AllMembers(result=result)

    async def validate_user_not_exist(self, company_id: int, user_id: int):
        query = select(member).where(member.c.company_id == company_id).where(member.c.user_id == user_id)
        member_exists = await self.db.fetch_one(query)
        if not member_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    async def create_company_admin(self, company_id: int, user_id: int) -> Member:
        update_member = {
            "user_role": "admin"
        }
        query = update(member).where(member.c.company_id == company_id).where(member.c.user_id == user_id).values(update_member)
        await self.db.execute(query=query)
        query_1 = select(member).where(member.c.company_id == company_id).where(member.c.user_id == user_id)
        updated_member = await self.db.fetch_one(query=query_1)
        return Member(**dict(updated_member))

    async def get_company_admins(self, company_id: int) -> AdminsList:
        query = select(member).where(member.c.company_id == company_id).where(member.c.user_role == "admin")
        admins = await self.db.fetch_all(query)
        return AdminsList(admins=[Member(**item) for item in admins])


    async def check_for_user_exist(self, company_id: int, user_id: int):
        query = select(member).where(member.c.company_id == company_id).where(member.c.user_id == user_id).where(member.c.user_role == "admin")
        user_db = await self.db.fetch_one(query=query)
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")


    async def delete_company_admin(self, company_id: int, user_id: int):
        query = delete(member).where(member.c.company_id == company_id).where(member.c.user_id == user_id).where(member.c.user_role == "admin")
        await self.db.execute(query=query)
