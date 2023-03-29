from sqlalchemy.sql import select, insert, delete
from databases import Database
from fastapi import HTTPException
from starlette import status
from models.models import action, member


from schemas.action_schemas import SendInviteRequest, AllUserInvites, Member, GetInviteRequest
from schemas.schemas import UserScheme


class InviteServices:
    def __init__(self, db: Database, current_user: UserScheme = None):
        self.db = db
        self.current_user_id = None if not current_user else current_user.user_id

    async def send_invite(self, invite: SendInviteRequest) -> GetInviteRequest:
        query = select(action).where(action.c.user_id == invite.user_id).where(action.c.company_id == invite.company_id)
        check_invite = await self.db.fetch_one(query)
        if check_invite:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite is already sent")
        new_invite = {
            "user_id": invite.user_id,
            "company_id": invite.company_id,
            "action_type": "invitation"
        }
        query = insert(action).values(new_invite)
        action_id = await self.db.execute(query=query)
        return GetInviteRequest(action_id=action_id,
                                 user_id=invite.user_id,
                                 company_id=invite.company_id,
                                 action_type="invitation"
        )

    async def get_my_invites(self) -> AllUserInvites:
        query = select(action).where(action.c.user_id == self.current_user_id).where(action.c.action_type == "invitation")
        result = await self.db.fetch_all(query)
        return AllUserInvites(result=[GetInviteRequest(**item) for item in result])

    async def get_company_invites(self, company_id: int) -> AllUserInvites:
        query = select(action).where(action.c.company_id == company_id).where(action.c.action_type == "invitation")
        result = await self.db.fetch_all(query)
        return AllUserInvites(result=[GetInviteRequest(**item) for item in result])

    async def company_cancel_invite(self, invite_id: int):
        query = delete(action).where(action.c.action_id == invite_id)
        await self.db.execute(query=query)

    async def company_accept_invite(self, invite: SendInviteRequest) -> Member:
        if self.current_user_id != invite.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not your invite")

        new_member = {
            "user_id": invite.user_id,
            "company_id": invite.company_id,
            "user_role": "user"
        }

        query = insert(member).values(new_member)
        new_member_id = await self.db.execute(query=query)

        query = delete(action).where(action.c.action_id == invite.action_id)
        await self.db.execute(query=query)

        return Member(member_id=new_member_id,
                      user_id=invite.user_id,
                      company_id=invite.company_id,
                      user_role="user"
        )

    async def company_decline_invite(self, invite: GetInviteRequest):
        if self.current_user_id != invite.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not your invite")
        query = delete(action).where(action.c.action_id == invite.action_id)
        await self.db.execute(query=query)

    async def check_action_for_exist(self, action_id: int) -> GetInviteRequest:
        query = select(action).where(action.c.action_id == action_id)
        action_from_db = await self.db.fetch_one(query=query)
        if not action_from_db:
            raise HTTPException(status_code=404, detail='Action does not exist')
        return GetInviteRequest(**dict(action_from_db))

