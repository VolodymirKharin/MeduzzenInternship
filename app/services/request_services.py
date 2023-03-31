from sqlalchemy.sql import select, insert, delete
from databases import Database
from fastapi import HTTPException
from starlette import status
from models.models import action, member, Company


from schemas.action_schemas import SendRequest, AllUserRequest, SendInviteRequest, Member, ResponseRequest, GetInviteRequest
from schemas.company_schemas import CompanyScheme
from schemas.user_schemas import UserScheme


class RequestServices:
    def __init__(self, db: Database, current_user: UserScheme = None):
        self.db = db
        self.current_user_id = None if not current_user else current_user.user_id

    async def send_request(self, request: SendRequest) -> GetInviteRequest:
        await self.check_current_user()
        query = select(action).where(action.c.user_id == self.current_user_id).where(action.c.company_id == request.company_id).where(action.c.action_type == "request")
        check_request = await self.db.fetch_one(query)
        if check_request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request is already sent")
        new_request = {
            "user_id": self.current_user_id,
            "company_id": request.company_id,
            "action_type": "request"
        }
        query = insert(action).values(new_request)
        action_id = await self.db.execute(query=query)
        return GetInviteRequest(action_id=action_id,
                                 user_id=self.current_user_id,
                                 company_id=request.company_id,
                                 action_type="request"
        )

    async def get_my_request(self) -> AllUserRequest:
        query = select(action).where(action.c.user_id == self.current_user_id)
        result = await self.db.fetch_all(query)
        return AllUserRequest(result=[GetInviteRequest(**item) for item in result])

    async def get_company_request(self, company_id: int) -> ResponseRequest:
        query = select(action).where(action.c.company_id == company_id).where(action.c.action_type == "request")
        result = await self.db.fetch_all(query)
        return [GetInviteRequest(**item) for item in result]

    async def company_accept_request(self, request: SendInviteRequest) -> Member:
        new_member = {
            "user_id": request.user_id,
            "company_id": request.company_id,
            "user_role": "user"
        }

        query = insert(member).values(new_member)
        new_member_id = await self.db.execute(query=query)

        query = delete(action).where(action.c.action_id == request.action_id)
        await self.db.execute(query=query)

        return Member(member_id=new_member_id,
                      user_id=request.user_id,
                      company_id=request.company_id,
                      user_role="user"
        )

    async def company_cancel_request(self, request: GetInviteRequest):
        if self.current_user_id != request.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your request")
        query = delete(action).where(action.c.action_id == request.action_id)
        await self.db.execute(query=query)

    async def company_decline_request(self, request: GetInviteRequest):
        query = delete(action).where(action.c.action_id == request.action_id)
        await self.db.execute(query=query)

    async def check_for_exist_member(self, company_id: int):
        query = select(member).where(member.c.company_id == company_id).where(member.c.user_id == self.current_user_id)
        company_db = await self.db.fetch_one(query=query)
        if company_db:
            raise HTTPException(status_code=403, detail="User is already a member of the company")

    async def check_for_owner(self, company_id: int):
        query = select(Company).where(Company.company_id == company_id)
        company_db = await self.db.fetch_one(query=query)
        check_company = CompanyScheme(**dict(company_db))
        if check_company.owner_id == self.current_user_id:
            raise HTTPException(status_code=403, detail="User is already a member of the company")

    async def check_not_owner(self, company_id: int, message: str):
        query = select(Company).where(Company.company_id == company_id)
        company_db = await self.db.fetch_one(query=query)
        check_company = CompanyScheme(**dict(company_db))
        if check_company.owner_id != self.current_user_id:
            raise HTTPException(status_code=403, detail=f"Only the owner of the company can {message} requests")

    async def check_current_user(self):
        if not self.current_user_id:
            raise HTTPException(status_code=403, detail="Not authenticated")

