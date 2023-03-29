from sqlalchemy.sql import select, delete
from databases import Database
from fastapi import HTTPException
from starlette import status
from models.models import member

from schemas.action_schemas import Member, AllMembers, MemberListResponse
from schemas.schemas import UserScheme


class MemberServices:
    def __init__(self, db: Database, current_user: UserScheme = None):
        self.db = db
        self.current_user_id = None if not current_user else current_user.user_id

    async def get_company_members(self) -> AllMembers:
        member_list = await self.db.fetch_all(query=select(member))
        result = MemberListResponse(users=[Member(**item) for item in member_list])
        return AllMembers(result=result)

    async def validate_member(self, company_id: int, user_id: int):
        query = select(member).where(member.c.company_id == company_id).where(member.c.user_id == user_id)
        member_exists = await self.db.fetch_one(query)
        if member_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member already exists")

    async def validate_member_not_exist(self, company_id: int, member_id: int):
        query = select(member).where(member.c.company_id == company_id).where(member.c.member_id == member_id)
        member_exists = await self.db.fetch_one(query)
        if not member_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    async def kick_member_from_company(self, company_id: int, member_id: int):
        query = delete(member).where(member.c.company_id == company_id).where(member.c.member_id == member_id)
        await self.db.execute(query=query)

    async def leave_member_from_company(self, company_id: int):
        query = delete(member).where(member.c.company_id == company_id).where(member.c.user_id == self.current_user_id)
        await self.db.execute(query=query)
