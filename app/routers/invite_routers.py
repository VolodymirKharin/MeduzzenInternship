from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from schemas.action_schemas import SendInviteRequest, Response, AllUserInvites, Member, AllMembers, GetInviteRequest,ResponseMember, SendRequest
from schemas.user_schemas import UserScheme

from services.invite_services import InviteServices
from services.member_services import MemberServices
from services.auth_services import get_current_user
from services.user_services import UserServices
from services.company_services import CompanyServices

from db.db_connection import get_db
from databases import Database


invite_routers = APIRouter(tags=["invite"])


@invite_routers.post("/invite", response_model=Response[GetInviteRequest], status_code=status.HTTP_201_CREATED)
async def send_invite(invite: SendInviteRequest, current_user: UserScheme = Depends(get_current_user),
                      db: Database = Depends(get_db)) -> Response[GetInviteRequest]:
    user_service = UserServices(db=db, current_user=current_user)
    await user_service.check_for_user_existing(user_id=invite.user_id)

    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_company_for_exist(company_id=invite.company_id)

    action_service = InviteServices(db=db)
    await company_service.check_for_owner(company_id=invite.company_id)

    if invite.user_id == current_user.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cant' invite yourself in your own company")
    member_service = MemberServices(db=db)
    await member_service.validate_member(company_id=invite.company_id, user_id=invite.user_id)
    new_invite = await action_service.send_invite(invite=invite)

    return Response(
        status_code=status.HTTP_201_CREATED,
        detail="success",
        result=new_invite
    )


@invite_routers.get("/invite/my", response_model=AllUserInvites, status_code=status.HTTP_200_OK)
async def get_user_invites(current_user: UserScheme = Depends(get_current_user),
                      db: Database = Depends(get_db)) -> AllUserInvites:
    action_service = InviteServices(db=db, current_user=current_user)
    my_invites = await action_service.get_my_invites()
    return AllUserInvites(result=my_invites.result)


@invite_routers.get("/invite/company/{company_id}", response_model=AllUserInvites, status_code=status.HTTP_200_OK)
async def get_company_invites(company_id: int, current_user: UserScheme = Depends(get_current_user),
                      db: Database = Depends(get_db)) -> AllUserInvites:
    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=company_id)

    action_service = InviteServices(db=db, current_user=current_user)
    company_invites = await action_service.get_company_invites(company_id=company_id)
    return AllUserInvites(result=company_invites.result)


@invite_routers.delete('/invite/{invite_id}')
async def company_cancel_invite(invite_id: int, db: Database = Depends(get_db), current_user: UserScheme = Depends(get_current_user)):
    action_service = InviteServices(db=db, current_user=current_user)
    invite = await action_service.check_action_for_exist(action_id=invite_id)

    company_service = CompanyServices(db=db, current_user=current_user)
    await company_service.check_for_owner(company_id=invite.company_id)

    await action_service.company_cancel_invite(invite_id=invite_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="deleted successfully")


@invite_routers.get('/invite/{invite_id}/accept', response_model=ResponseMember[Member], status_code=status.HTTP_200_OK)
async def user_accept_invite(invite_id: int, db: Database = Depends(get_db),
                                current_user: UserScheme = Depends(get_current_user)) -> ResponseMember[Member]:

    action_service = InviteServices(db=db, current_user=current_user)
    invite = await action_service.check_action_for_exist(action_id=invite_id)

    new_member = await action_service.company_accept_invite(invite=invite)
    return ResponseMember(
        status_code=200,
        detail="success",
        result=new_member
    )


@invite_routers.get('/invite/{invite_id}/decline', response_model=Response[Member], status_code=status.HTTP_200_OK)
async def user_decline_invite(invite_id: int, db: Database = Depends(get_db),
                             current_user: UserScheme = Depends(get_current_user)) -> Response[Member]:
    action_service = InviteServices(db=db, current_user=current_user)
    invite = await action_service.check_action_for_exist(action_id=invite_id)
    await action_service.company_decline_invite(invite=invite)
    return Response(
        status_code=200,
        detail="success",
    )


